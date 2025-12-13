require_relative 'abstract_command_handler'

class ArrayHandler < AbstractCommandHandler
  def process(command)
    begin
      processed_array = command.payload
      return processed_array
    rescue Exception => e
      return e
    end
  end
end
