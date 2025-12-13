require_relative 'abstract_command_handler'

class LoadLibraryHandler < AbstractCommandHandler

  @@loaded_libraries = []

  def initialize
    @required_parameters_count = 1
  end

  def process(command)
    begin
      if command.payload.length < @required_parameters_count
        raise ArgumentError.new "Load library parameters mismatch"
      end

      assembly_name =
        if command.payload.length > @required_parameters_count
          command.payload[1]
        else
          command.payload[0]
        end

      # Normalize to absolute path
      expanded_path = File.expand_path(assembly_name)

      # Load only once per absolute path
      if @@loaded_libraries.include?(expanded_path)
        return 0
      end

      # Check if the library exists:
      raise LoadError.new("Library not found: #{assembly_name}") unless File.exist?(expanded_path)

      # Require by path; Ruby will also avoid re-loading the same feature,
      # but we additionally track it ourselves.
      require expanded_path

      @@loaded_libraries << expanded_path
      return 0
    rescue Exception => e
      return e
    end
  end

  def self.get_loaded_libraries
    @@loaded_libraries
  end
end
