class RuntimeLogger
  @not_logged_yet = true

  def self.get_runtime_info(get_loaded_modules)
    begin
      pieces = []
      pieces << to_utf8("Ruby Managed Runtime Info:\n")
      pieces << to_utf8("Ruby Version: #{RUBY_VERSION}\n")
      pieces << to_utf8("Ruby Implementation: #{RUBY_ENGINE}\n")
      pieces << to_utf8("Ruby Platform: #{RUBY_PLATFORM}\n")
      pieces << to_utf8("Ruby Engine: #{RUBY_ENGINE}\n")
      pieces << to_utf8("Ruby Engine Version: #{RUBY_ENGINE_VERSION}\n")
      pieces << to_utf8("Current Directory: #{Dir.pwd}\n")
      paths = $LOAD_PATH.map { |p| to_utf8(p.to_s) }.join(", ")
      pieces << to_utf8("Ruby search path: ") + paths + to_utf8("\n")

      if get_loaded_modules
        loaded = $LOADED_FEATURES.map(&:to_s).reject { |feature| feature.include?("Binaries/Ruby") }.join(", ")
        pieces << to_utf8("Ruby loaded modules (excluding Javonet classes): " + loaded + "\n")
      end

      pieces.join
    rescue => e
      to_utf8("Ruby Managed Runtime Info: Error while fetching runtime info")
    end
  end

  def self.print_runtime_info(get_loaded_modules = true)
    if @not_logged_yet
      puts get_runtime_info(get_loaded_modules)
      @not_logged_yet = false
    end
  end

  private_class_method def self.to_utf8(value)
    str = value.to_s
    # set encoding to UTF-8 and handle invalid byte sequences
    str.encode('UTF-8', 'binary', invalid: :replace, undef: :replace, replace: '?')
  rescue Encoding::UndefinedConversionError, Encoding::InvalidByteSequenceError
    # Fallback: force encoding to UTF-8 and replace invalid/undefined characters
    str.force_encoding('UTF-8').encode('UTF-8', invalid: :replace, undef: :replace, replace: '?')
  rescue
    # In case of any other error, return a simple string
    value.to_s
  end
end
