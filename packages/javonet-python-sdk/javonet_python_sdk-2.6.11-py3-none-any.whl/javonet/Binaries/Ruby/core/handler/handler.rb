require_relative '../../utils/runtime_name_javonet'
require_relative '../../utils/command_type'
require_relative '../../utils/command'
require_relative '../../utils/types_handler'

require_relative '../../utils/exceptions/exception_serializer'

require_relative '../../core/reference_cache/references_cache'

require_relative '../../core/handler/handler_dictionary'
require_relative '../../core/handler/abstract_handler'
require_relative '../../core/handler/value_handler'
require_relative '../../core/handler/load_library_handler'
require_relative '../../core/handler/invoke_static_method_handler'
require_relative '../../core/handler/get_static_field_handler'
require_relative '../../core/handler/set_static_field_handler'
require_relative '../../core/handler/create_class_instance_handler'
require_relative '../../core/handler/get_type_handler'
require_relative '../../core/handler/resolve_instance_handler'
require_relative '../../core/handler/get_module_handler'
require_relative '../../core/handler/invoke_instance_method_handler'
require_relative '../../core/handler/exception_handler'
require_relative '../../core/handler/heartbeat_handler'
require_relative '../../core/handler/casting_handler'
require_relative '../../core/handler/get_instance_field_handler'
require_relative '../../core/handler/optimize_handler'
require_relative '../../core/handler/generate_lib_handler'
require_relative '../../core/handler/invoke_global_function_handler'
require_relative '../../core/handler/destruct_reference_handler'
require_relative '../../core/handler/array_reference_handler'
require_relative '../../core/handler/array_get_item_handler'
require_relative '../../core/handler/array_get_size_handler'
require_relative '../../core/handler/array_get_rank_handler'
require_relative '../../core/handler/array_set_item_handler'
require_relative '../../core/handler/array_handler'
require_relative '../../core/handler/retrieve_array_handler'
require_relative '../../core/handler/set_instance_field_handler'
require_relative '../../core/handler/invoke_generic_static_method_handler'
require_relative '../../core/handler/invoke_generic_method_handler'
require_relative '../../core/handler/get_enum_item_handler'
require_relative '../../core/handler/get_enum_name_handler'
require_relative '../../core/handler/get_enum_value_handler'
require_relative '../../core/handler/as_ref_handler'
require_relative '../../core/handler/as_out_handler'
require_relative '../../core/handler/get_ref_value_handler'
require_relative '../../core/handler/enable_namespace_handler'
require_relative '../../core/handler/enable_type_handler'
require_relative '../../core/handler/create_null_handler'
require_relative '../../core/handler/get_static_method_as_delegate_handler'
require_relative '../../core/handler/get_instance_method_as_delegate_handler'
require_relative '../../core/handler/pass_delegate_handler'
require_relative '../../core/handler/invoke_delegate_handler'
require_relative '../../core/handler/convert_type_handler'
require_relative '../../core/handler/add_event_listener_handler'
require_relative '../../core/handler/plugin_wrapper_handler'
require_relative '../../core/handler/get_async_operation_result_handler'
require_relative '../../core/handler/as_kwargs_handler'
require_relative '../../core/handler/get_result_type_handler'
require_relative '../../core/handler/get_global_field_handler'
require_relative '../../core/handler/register_for_update_handler'
require_relative '../../core/handler/value_for_update_handler'

class Handler < AbstractHandler
  def self.initialize_handler_dict
    return unless $handler_dict.empty?

    value_handler = ValueHandler.new
    load_library_handler = LoadLibraryHandler.new
    invoke_static_method_handler = InvokeStaticMethodHandler.new
    get_static_field_handler = GetStaticFieldHandler.new
    set_static_field_handler = SetStaticFieldHandler.new
    create_class_instance_handler = CreateClassInstanceHandler.new
    get_type_handler = GetTypeHandler.new
    resolve_instance_handler = ResolveInstanceHandler.new
    get_module_handler = GetModuleHandler.new
    invoke_instance_method_handler = InvokeInstanceMethodHandler.new
    exception_handler = ExceptionHandler.new
    heartbeat_handler = HeartbeatHandler.new
    casting_handler = CastingHandler.new
    get_instance_field_handler = GetInstanceFieldHandler.new
    optimize_handler = OptimizeHandler.new
    generate_lib_handler = GenerateLibHandler.new
    invoke_global_function_handler = InvokeGlobalFunctionHandler.new
    destruct_reference_handler = DestructReferenceHandler.new
    array_reference_handler = ArrayReferenceHandler.new
    array_get_item_handler = ArrayGetItemHandler.new
    array_get_size_handler = ArrayGetSizeHandler.new
    array_get_rank_handler = ArrayGetRankHandler.new
    array_set_item_handler = ArraySetItemHandler.new
    array_handler = ArrayHandler.new
    retrieve_array_handler = RetrieveArrayHandler.new
    set_instance_field_handler = SetInstanceFieldHandler.new
    invoke_generic_static_method_handler = InvokeGenericStaticMethodHandler.new
    invoke_generic_method_handler = InvokeGenericMethodHandler.new
    get_enum_item_handler = GetEnumItemHandler.new
    get_enum_name_handler = GetEnumNameHandler.new
    get_enum_value_handler = GetEnumValueHandler.new
    as_ref_handler = AsRefHandler.new
    as_out_handler = AsOutHandler.new
    get_ref_value_handler = GetRefValueHandler.new
    enable_namespace_handler = EnableNamespaceHandler.new
    enable_type_handler = EnableTypeHandler.new
    create_null_handler = CreateNullHandler.new
    get_static_method_as_delegate_handler = GetStaticMethodAsDelegateHandler.new
    get_instance_method_as_delegate_handler = GetInstanceMethodAsDelegateHandler.new
    pass_delegate_handler = PassDelegateHandler.new
    invoke_delegate_handler = InvokeDelegateHandler.new
    convert_type_handler = ConvertTypeHandler.new
    add_event_listener_handler = AddEventListenerHandler.new
    plugin_wrapper_handler = PluginWrapperHandler.new
    get_async_operation_result_handler = GetAsyncOperationResultHandler.new
    as_kwargs_handler = AsKwargsHandler.new
    get_result_type_handler = GetResultTypeHandler.new
    get_global_field_handler = GetGlobalFieldHandler.new
    register_for_update_handler = RegisterForUpdateHandler.new
    value_for_update_handler = ValueForUpdateHandler.new

    $handler_dict[CommandType::VALUE] = value_handler
    $handler_dict[CommandType::LOAD_LIBRARY] = load_library_handler
    $handler_dict[CommandType::INVOKE_STATIC_METHOD] = invoke_static_method_handler
    $handler_dict[CommandType::GET_STATIC_FIELD] = get_static_field_handler
    $handler_dict[CommandType::SET_STATIC_FIELD] = set_static_field_handler
    $handler_dict[CommandType::CREATE_CLASS_INSTANCE] = create_class_instance_handler
    $handler_dict[CommandType::GET_TYPE] = get_type_handler
    $handler_dict[CommandType::REFERENCE] = resolve_instance_handler
    $handler_dict[CommandType::GET_MODULE] = get_module_handler
    $handler_dict[CommandType::INVOKE_INSTANCE_METHOD] = invoke_instance_method_handler
    $handler_dict[CommandType::EXCEPTION] = exception_handler
    $handler_dict[CommandType::HEARTBEAT] = heartbeat_handler
    $handler_dict[CommandType::CAST] = casting_handler
    $handler_dict[CommandType::GET_INSTANCE_FIELD] = get_instance_field_handler
    $handler_dict[CommandType::OPTIMIZE] = optimize_handler
    $handler_dict[CommandType::GENERATE_LIB] = generate_lib_handler
    $handler_dict[CommandType::INVOKE_GLOBAL_FUNCTION] = invoke_global_function_handler
    $handler_dict[CommandType::DESTRUCT_REFERENCE] = destruct_reference_handler
    $handler_dict[CommandType::ARRAY_REFERENCE] = array_reference_handler
    $handler_dict[CommandType::ARRAY_GET_ITEM] = array_get_item_handler
    $handler_dict[CommandType::ARRAY_GET_SIZE] = array_get_size_handler
    $handler_dict[CommandType::ARRAY_GET_RANK] = array_get_rank_handler
    $handler_dict[CommandType::ARRAY_SET_ITEM] = array_set_item_handler
    $handler_dict[CommandType::ARRAY] = array_handler
    $handler_dict[CommandType::RETRIEVE_ARRAY] = retrieve_array_handler
    $handler_dict[CommandType::SET_INSTANCE_FIELD] = set_instance_field_handler
    $handler_dict[CommandType::INVOKE_GENERIC_STATIC_METHOD] = invoke_generic_static_method_handler
    $handler_dict[CommandType::INVOKE_GENERIC_METHOD] = invoke_generic_method_handler
    $handler_dict[CommandType::GET_ENUM_ITEM] = get_enum_item_handler
    $handler_dict[CommandType::GET_ENUM_NAME] = get_enum_name_handler
    $handler_dict[CommandType::GET_ENUM_VALUE] = get_enum_value_handler
    $handler_dict[CommandType::AS_REF] = as_ref_handler
    $handler_dict[CommandType::AS_OUT] = as_out_handler
    $handler_dict[CommandType::GET_REF_VALUE] = get_ref_value_handler
    $handler_dict[CommandType::ENABLE_NAMESPACE] = enable_namespace_handler
    $handler_dict[CommandType::ENABLE_TYPE] = enable_type_handler
    $handler_dict[CommandType::CREATE_NULL] = create_null_handler
    $handler_dict[CommandType::GET_STATIC_METHOD_AS_DELEGATE] = get_static_method_as_delegate_handler
    $handler_dict[CommandType::GET_INSTANCE_METHOD_AS_DELEGATE] = get_instance_method_as_delegate_handler
    $handler_dict[CommandType::PASS_DELEGATE] = pass_delegate_handler
    $handler_dict[CommandType::INVOKE_DELEGATE] = invoke_delegate_handler
    $handler_dict[CommandType::CONVERT_TYPE] = convert_type_handler
    $handler_dict[CommandType::ADD_EVENT_LISTENER] = add_event_listener_handler
    $handler_dict[CommandType::PLUGIN_WRAPPER] = plugin_wrapper_handler
    $handler_dict[CommandType::GET_ASYNC_OPERATION_RESULT] = get_async_operation_result_handler
    $handler_dict[CommandType::AS_KWARGS] = as_kwargs_handler
    $handler_dict[CommandType::GET_RESULT_TYPE] = get_result_type_handler
    $handler_dict[CommandType::GET_GLOBAL_FIELD] = get_global_field_handler
    $handler_dict[CommandType::REGISTER_FOR_UPDATE] = register_for_update_handler
    $handler_dict[CommandType::VALUE_FOR_UPDATE] = value_for_update_handler
  end

  def self.handle_command(command)
    initialize_handler_dict
    begin
      if command.command_type == CommandType::RETRIEVE_ARRAY
        response_array = $handler_dict[CommandType::REFERENCE].handle_command(command.payload[0])
        return Command.create_array_response(response_array, command.runtime_name)
      end

      response = $handler_dict[command.command_type].handle_command(command)

      if response.is_a? Exception
        ExceptionSerializer.serialize_exception(response, command)
      else
        parse_response(response, command.runtime_name)
      end
    rescue Exception => e
      ExceptionSerializer.serialize_exception(e, command)
    end
  end

  private

  def self.parse_response(response, runtime_name)
    # Build base response (primitive vs reference)
    response_command =
      if TypesHandler.primitive_or_none?(response)
        Command.create_response(response, runtime_name)
      else
        reference_cache = ReferencesCache.instance
        guid = reference_cache.cache_reference(response)
        Command.create_reference(guid, runtime_name)
      end

    # Append ValueForUpdate commands from invocation contexts if present
    invocation_contexts = RegisterForUpdateHandler.get_or_create_context_dict
    if invocation_contexts && !invocation_contexts.empty?
      ref_cache = ReferencesCache.instance
      invocation_contexts.each do |key, value|
        instance_guid = ref_cache.cache_reference(value)
        update_context_command = Command.new(
          runtime_name,
          CommandType::VALUE_FOR_UPDATE,
          [key.to_s,
           instance_guid]
        )
        response_command = response_command.add_arg_to_payload(update_context_command)
      end
      # Clear all entries after processing this request
      invocation_contexts.clear
    end

    response_command
  end

  def self.is_response_array(response)
    response.is_a? Array
  end
end
