require_relative './exception_type'

class ExceptionSerializer

  def self.serialize_exception(exception, command)
    exception_command = Command.new(command.runtime_name, CommandType::EXCEPTION, [])
    begin
      stack_trace = exception.backtrace
      exception_message = exception.message
      exception_name = exception.class.to_s

      stack_classes = ""
      stack_methods = ""
      stack_lines = ""
      stack_files = ""
      if !stack_trace.nil? && !stack_trace.empty?
        stack_trace.each_with_index do |value, index|
          stack_file, stack_class, stack_line, stack_method = parse_stack_frame(value)
          unless stack_file.include?("javonet-ruby-sdk") or stack_file.include?("Binaries/Ruby")
            append_to_string(stack_classes, stack_class)
            append_to_string(stack_methods, stack_method)
            append_to_string(stack_lines, stack_line)
            append_to_string(stack_files, stack_file)
            if index != stack_trace.length - 1
              append_to_string(stack_classes, "|")
              append_to_string(stack_methods, "|")
              append_to_string(stack_lines, "|")
              append_to_string(stack_files, "|")
            end
          end
        end
      end

      exception_command = exception_command.add_arg_to_payload(get_exception_code(exception_name.to_s))
      exception_command = exception_command.add_arg_to_payload(command.to_string)
      exception_command = exception_command.add_arg_to_payload(exception_name.to_s)
      exception_command = exception_command.add_arg_to_payload(exception_message)
      exception_command = exception_command.add_arg_to_payload(stack_classes)
      exception_command = exception_command.add_arg_to_payload(stack_methods)
      exception_command = exception_command.add_arg_to_payload(stack_lines)
      exception_command = exception_command.add_arg_to_payload(stack_files)
    rescue Exception => e
      exception_command = Command.new(RuntimeNameJavonet::RUBY, CommandType::EXCEPTION, [])
      exception_command = exception_command.add_arg_to_payload(ExceptionType::EXCEPTION)
      if command.nil?
        exception_command = exception_command.add_arg_to_payload("Command is nil")
      else
        exception_command = exception_command.add_arg_to_payload(command.to_string)
      end
      exception_command = exception_command.add_arg_to_payload("Ruby Exception Serialization Error")
      exception_command = exception_command.add_arg_to_payload(e.message)
      exception_command = exception_command.add_arg_to_payload("ExceptionSerializer")
      exception_command = exception_command.add_arg_to_payload("serialize_exception")
      exception_command = exception_command.add_arg_to_payload("undefined")
      exception_command = exception_command.add_arg_to_payload(__FILE__)
    end
    exception_command
  end

  def self.append_to_string(string, value)
    if value.nil?
      string << "undefined"
    else
      string << value
    end
  end

  def self.parse_stack_frame(stack_frame)
    match = /^(.+):(\d+):in [`'](.+)[`']$/.match(stack_frame)
    return ["undefined", "undefined", "undefined", "undefined"] if match.nil?

    stack_file, stack_line, method_info = match.captures

    case method_info
    when /^(.+)#(.+)$/
      stack_class = $1.split('::').last || 'undefined'
      stack_method = $2
    when /^(.+)\.(.+)$/
      # handle Class.method
      stack_class = $1.split('::').last || 'undefined'
      stack_method = $2
    when /^<(.+)>$/
      stack_class = 'undefined'
      stack_method = "<#{$1}>"
    else
      # no class information — e.g. top-level method or block
      stack_class = 'undefined'
      stack_method = method_info
    end

    [stack_file, stack_class, stack_line, stack_method]
  end

  def self.get_exception_code(exception_name)
    case exception_name
    when "Exception"
      return ExceptionType::EXCEPTION
    when "IOError"
      return ExceptionType::IO_EXCEPTION
    when "Errno::ENOENT"
      return ExceptionType::FILE_NOT_FOUND_EXCEPTION
    when "RuntimeError"
      return ExceptionType::RUNTIME_EXCEPTION
    when "ZeroDivisionError"
      return ExceptionType::ARITHMETIC_EXCEPTION
    when "ArgumentError"
      return ExceptionType::ILLEGAL_ARGUMENT_EXCEPTION
    when "IndexError"
      return ExceptionType::INDEX_OUT_OF_BOUNDS_EXCEPTION
    when "TypeError"
      return ExceptionType::NULL_POINTER_EXCEPTION
    else
      return ExceptionType::EXCEPTION
    end
  end
end
