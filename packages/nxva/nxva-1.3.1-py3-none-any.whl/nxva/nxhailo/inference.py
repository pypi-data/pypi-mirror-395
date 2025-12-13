import os
import threading


class HefInference:
    import resource
    # ---- class-level shared state ----
    in_format, out_format = None, None
    interface = None
    target = None
    active_model_id = None
    network_context = None
    infer_pipeline = None
    models_pool = {}
    model_num = 0

    # 串行化所有「切換/推論」操作的鎖
    _lock = threading.RLock()

    # 避免 core dump / 關掉 hailo logger
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.environ["HAILORT_LOGGER_PATH"] = "NONE"

    def __init__(self, weight):
        self.load_model(weight)

    def load_model(self, weight):
        from hailo_platform import (
            VDevice, HEF, HailoStreamInterface, ConfigureParams,
            InputVStreamParams, OutputVStreamParams, FormatType
        )
        # 不需要鎖：只要 pool 是空才會建 VDevice；多執行緒時仍建議加鎖保險
        with HefInference._lock:
            if not HefInference.models_pool:
                HefInference.target = VDevice()

            try:
                self.model_id = HefInference.model_num
                HefInference.model_num += 1

                hef = HEF(weight)
                configure_params = ConfigureParams.create_from_hef(
                    hef, interface=HailoStreamInterface.PCIe
                )
                network_group = HefInference.target.configure(hef, configure_params)[0]
                network_group_params = network_group.create_params()

                # vstream params
                input_vstreams_params = InputVStreamParams.make(
                    network_group, format_type=FormatType.FLOAT32
                )
                output_vstreams_params = OutputVStreamParams.make(
                    network_group, format_type=FormatType.FLOAT32
                )

                HefInference.models_pool[self.model_id] = {
                    "hef": hef,
                    "network_group": network_group,
                    "network_group_params": network_group_params,
                    "input_vstreams_params": input_vstreams_params,
                    "output_vstreams_params": output_vstreams_params,
                    "input_info": [n.name for n in hef.get_input_vstream_infos()],
                    "output_infos": hef.get_output_vstream_infos(),
                }
            except Exception as e:
                HefInference.model_num -= 1
                raise ValueError(f"Error loading model {getattr(self, 'model_id', '?')}: {e}")

    @classmethod
    def _activate_model(cls, model_id):
        # 僅允許單執行緒進入（切換與 context 進出都在鎖內）
        from hailo_platform import InferVStreams
        m = cls.models_pool[model_id]

        # 關掉舊的（若存在）
        if cls.infer_pipeline is not None:
            try:
                cls.infer_pipeline.__exit__(None, None, None)
            finally:
                cls.infer_pipeline = None
        if cls.network_context is not None:
            try:
                cls.network_context.__exit__(None, None, None)
            finally:
                cls.network_context = None

        # 啟動新的
        cls.network_context = m["network_group"].activate(m["network_group_params"])
        cls.infer_pipeline = InferVStreams(
            m["network_group"],
            m["input_vstreams_params"],
            m["output_vstreams_params"],
        )
        cls.network_context.__enter__()
        cls.infer_pipeline.__enter__()
        cls.active_model_id = model_id

    def switch_model(self):
        # 使用 class-level 鎖，避免和推論並行
        with HefInference._lock:
            if self.model_id not in HefInference.models_pool:
                raise ValueError(f"Model {self.model_id} not found in pool")
            if self.model_id == HefInference.active_model_id:
                return
            HefInference._activate_model(self.model_id)

    def __call__(self, input_data):
        # 同樣鎖起來：保證不會在別人切換時推論，反之亦然
        with HefInference._lock:
            # 確保 active model 正確
            if self.model_id != HefInference.active_model_id: self.switch_model()
            return HefInference.infer_pipeline.infer(input_data)

    def close(self):
        # 關閉也鎖一下，避免 race
        with HefInference._lock:
            try:
                if HefInference.infer_pipeline is not None:
                    HefInference.infer_pipeline.__exit__(None, None, None)
                    HefInference.infer_pipeline = None
                if HefInference.network_context is not None:
                    HefInference.network_context.__exit__(None, None, None)
                    HefInference.network_context = None
                if HefInference.target is not None:
                    HefInference.target.release()
                    HefInference.target = None
                HefInference.active_model_id = None
            except Exception:
                # 關閉階段通常不 raise，避免卡住上層
                pass