from typing import override

from ai_parade._toolkit.enums import ModelFormat
from ai_parade._toolkit.run.ModelRunner import ModelRunner
from ai_parade._toolkit.run.ONNX import ONNXRunner

from .converter import ConverterOptions, FormatConverter


class ONNX2TensorFlowConverter(FormatConverter):
	"""
	https://github.com/PINTO0309/onnx2tf
	"""

	@property
	@override
	def format_conversion(self):
		return (ModelFormat.ONNX, ModelFormat.SavedModel)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.convert

	def convert(self, runner: ModelRunner):
		assert isinstance(runner, ONNXRunner)
		from onnx2tf import convert  # type: ignore

		convert(
			input_onnx_file_path=runner.weights,
			output_folder_path=runner.output_directory / self._output_weights,
			# output_signaturedefs: Optional[bool] = False,
			# output_h5: Optional[bool] = False,
			# output_keras_v3: Optional[bool] = False,
			# output_tfv1_pb: Optional[bool] = False,
			# output_weights: Optional[bool] = False,
			# copy_onnx_input_output_names_to_tflite: Optional[bool] = False,
			# output_integer_quantized_tflite: Optional[bool] = False,
			# quant_type: Optional[str] = 'per-channel',
			# custom_input_op_name_np_data_path: Optional[List] = None,
			# input_quant_dtype: Optional[str] = 'int8',
			# output_quant_dtype: Optional[str] = 'int8',
			# not_use_onnxsim: Optional[bool] = False,
			# not_use_opname_auto_generate: Optional[bool] = False,
			# batch_size: Union[int, NoneType] = None,
			# overwrite_input_shape: Union[List[str], NoneType] = None,
			# no_large_tensor: Optional[bool] = False,
			# output_nms_with_dynamic_tensor: Optional[bool] = False,
			# keep_ncw_or_nchw_or_ncdhw_input_names: Union[List[str], NoneType] = None,
			# keep_nwc_or_nhwc_or_ndhwc_input_names: Union[List[str], NoneType] = None,
			# keep_shape_absolutely_input_names: Optional[List[str]] = None,
			# input_names_to_interrupt_model_conversion: Union[List[str], NoneType] = None,
			# output_names_to_interrupt_model_conversion: Union[List[str], NoneType] = None,
			# disable_group_convolution: Union[bool, NoneType] = False,
			# enable_batchmatmul_unfold: Optional[bool] = False,
			# enable_rnn_unroll: Optional[bool] = False,
			# disable_suppression_flextranspose: Optional[bool] = False,
			# number_of_dimensions_after_flextranspose_compression: Optional[int] = 6,
			# disable_suppression_flexstridedslice: Optional[bool] = False,
			# disable_strict_mode: Optional[bool] = False,
			# number_of_dimensions_after_flexstridedslice_compression: Optional[int] = 5,
			# optimization_for_gpu_delegate: Optional[bool] = False,
			# replace_argmax_to_reducemax_and_indices_is_int64: Union[bool, NoneType] = False,
			# replace_argmax_to_reducemax_and_indices_is_float32: Union[bool, NoneType] = False,
			# replace_argmax_to_fused_argmax_and_indices_is_int64: Union[bool, NoneType] = False,
			# replace_argmax_to_fused_argmax_and_indices_is_float32: Union[bool, NoneType] = False,
			# fused_argmax_scale_ratio: Union[float, NoneType] = 0.5,
			# replace_to_pseudo_operators: List[str] = None,
			# mvn_epsilon: Union[float, NoneType] = 0.0000000001,
			# param_replacement_file: Optional[str] = '',
			# check_gpu_delegate_compatibility: Optional[bool] = False,
			# check_onnx_tf_outputs_elementwise_close: Optional[bool] = False,
			# check_onnx_tf_outputs_elementwise_close_full: Optional[bool] = False,
			# check_onnx_tf_outputs_sample_data_normalization: Optional[str] = 'norm',
			# check_onnx_tf_outputs_elementwise_close_rtol: Optional[float] = 0.0,
			# check_onnx_tf_outputs_elementwise_close_atol: Optional[float] = 1e-4,
			# disable_model_save: Union[bool, NoneType] = False,
			# non_verbose: Union[bool, NoneType] = False,
			# verbosity: Optional[str] = 'debug'
		)

		return self._output_weights
