<?php

declare(strict_types=1);

namespace core\handler;

use ArrayObject;
use core\referencecache\ReferencesCache;
use core\referencecache\ArrayWrapper;
use Throwable;
use TypeError;
use utils\Command;
use utils\CommandInterface;
use utils\ExceptionSerializer;
use utils\type\CommandType;
use utils\TypesHandler;

final class Handler
{
    private static array $handlers = [];

    private function __construct()
    {
    }

    private static function initializeHandlers(): void
    {
        if (!empty(self::$handlers)) {
            return;
        }

        self::$handlers[CommandType::VALUE()->getValue()] = new ValueHandler();
        self::$handlers[CommandType::LOAD_LIBRARY()->getValue()] = new LoadLibraryHandler();
        self::$handlers[CommandType::INVOKE_STATIC_METHOD()->getValue()] = new InvokeStaticMethodHandler();
        self::$handlers[CommandType::GET_STATIC_FIELD()->getValue()] = new GetStaticFieldHandler();
        self::$handlers[CommandType::SET_STATIC_FIELD()->getValue()] = new SetStaticFieldHandler();
        self::$handlers[CommandType::CREATE_INSTANCE()->getValue()] = new CreateInstanceHandler();
        self::$handlers[CommandType::GET_TYPE()->getValue()] = new GetTypeHandler();
        self::$handlers[CommandType::REFERENCE()->getValue()] = new ResolveInstanceHandler();
        self::$handlers[CommandType::GET_MODULE()->getValue()] = new GetModuleHandler();
        self::$handlers[CommandType::INVOKE_INSTANCE_METHOD()->getValue()] = new InvokeInstanceMethodHandler();
        self::$handlers[CommandType::EXCEPTION()->getValue()] = new ExceptionHandler();
        self::$handlers[CommandType::HEART_BEAT()->getValue()] = new HeartBeatHandler();
        self::$handlers[CommandType::CAST()->getValue()] = new CastHandler();
        self::$handlers[CommandType::GET_INSTANCE_FIELD()->getValue()] = new GetInstanceFieldHandler();
        self::$handlers[CommandType::OPTIMIZE()->getValue()] = new OptimizeHandler();
        self::$handlers[CommandType::GENERATE_LIB()->getValue()] = new GenerateLibHandler();
        self::$handlers[CommandType::INVOKE_GLOBAL_FUNCTION()->getValue()] = new InvokeGlobalFunctionHandler();
        self::$handlers[CommandType::DESTRUCT_REFERENCE()->getValue()] = new DestructReferenceHandler();
        self::$handlers[CommandType::ARRAY_REFERENCE()->getValue()] = new ArrayReferenceHandler();
        self::$handlers[CommandType::ARRAY_GET_ITEM()->getValue()] = new ArrayGetItemHandler();
        self::$handlers[CommandType::ARRAY_GET_SIZE()->getValue()] = new ArrayGetSizeHandler();
        self::$handlers[CommandType::ARRAY_GET_RANK()->getValue()] = new ArrayGetRankHandler();
        self::$handlers[CommandType::ARRAY_SET_ITEM()->getValue()] = new ArraySetItemHandler();
        self::$handlers[CommandType::ARRAY()->getValue()] = new ArrayHandler();
        self::$handlers[CommandType::RETRIEVE_ARRAY()->getValue()] = null; // obsługiwane osobno
        self::$handlers[CommandType::SET_INSTANCE_FIELD()->getValue()] = new SetInstanceFieldHandler();
        self::$handlers[CommandType::INVOKE_GENERIC_STATIC_METHOD()->getValue()] = new InvokeGenericStaticMethodHandler();
        self::$handlers[CommandType::INVOKE_GENERIC_METHOD()->getValue()] = new InvokeGenericMethodHandler();
        self::$handlers[CommandType::GET_ENUM_ITEM()->getValue()] = new GetEnumItemHandler();
        self::$handlers[CommandType::GET_ENUM_NAME()->getValue()] = new GetEnumNameHandler();
        self::$handlers[CommandType::GET_ENUM_VALUE()->getValue()] = new GetEnumValueHandler();
        self::$handlers[CommandType::AS_REF()->getValue()] = new AsRefHandler();
        self::$handlers[CommandType::AS_OUT()->getValue()] = new AsOutHandler();
        self::$handlers[CommandType::GET_REF_VALUE()->getValue()] = new GetRefValueHandler();
        self::$handlers[CommandType::ENABLE_NAMESPACE()->getValue()] = new EnableNamespaceHandler();
        self::$handlers[CommandType::ENABLE_TYPE()->getValue()] = new EnableTypeHandler();
        self::$handlers[CommandType::CREATE_NULL()->getValue()] = new CreateNullHandler();
        self::$handlers[CommandType::GET_STATIC_METHOD_AS_DELEGATE()->getValue()] = new GetStaticMethodAsDelegateHandler();
        self::$handlers[CommandType::GET_INSTANCE_METHOD_AS_DELEGATE()->getValue()] = new GetInstanceMethodAsDelegateHandler();
        self::$handlers[CommandType::PASS_DELEGATE()->getValue()] = new PassDelegateHandler();
        self::$handlers[CommandType::INVOKE_DELEGATE()->getValue()] = new InvokeDelegateHandler();
        self::$handlers[CommandType::CONVERT_TYPE()->getValue()] = new ConvertTypeHandler();
        self::$handlers[CommandType::ADD_EVENT_LISTENER()->getValue()] = new AddEventListenerHandler();
        self::$handlers[CommandType::PLUGIN_WRAPPER()->getValue()] = new PluginWrapperHandler();
        self::$handlers[CommandType::GET_ASYNC_OPERATION_RESULT()->getValue()] = new GetAsyncOperationResultHandler();
        self::$handlers[CommandType::AS_KWARGS()->getValue()] = new AsKwargsHandler();
        self::$handlers[CommandType::GET_RESULT_TYPE()->getValue()] = new GetResultTypeHandler();
        self::$handlers[CommandType::GET_GLOBAL_FIELD()->getValue()] = new GetGlobalFieldHandler();
    }

    public static function getHandlers(): array
    {
        self::initializeHandlers();
        return self::$handlers;
    }

    public static function handleCommand(CommandInterface $command): CommandInterface
    {
        try {
            if ($command->getCommandType()->equalsByValue(CommandType::RETRIEVE_ARRAY)) {
                self::initializeHandlers();
                $resolvedObject = self::$handlers[CommandType::REFERENCE()->getValue()]->handleCommand($command->getPayload()[0]);

                if ($resolvedObject instanceof ArrayWrapper) {
                    return Command::createArrayResponse(
                        $resolvedObject->getData(),
                        $command->getRuntimeName()
                    );
                }

                if ($resolvedObject instanceof ArrayObject) {
                    return Command::createArrayResponse(
                        $resolvedObject->getArrayCopy(),
                        $command->getRuntimeName()
                    );
                }

                if (is_array($resolvedObject)) {
                    return Command::createArrayResponse(
                        $resolvedObject,
                        $command->getRuntimeName()
                    );
                }

                throw new TypeError(sprintf(
                    'Expected array, ArrayObject or ArrayWrapper for RETRIEVE_ARRAY, got %s',
                    is_object($resolvedObject) ? get_class($resolvedObject) : gettype($resolvedObject)
                ));
            }

            return self::getParseResponse($command);
        } catch (Throwable $e) {
            if ($e->getPrevious() !== null) {
                return ExceptionSerializer::serializeException($e->getPrevious(), $command);
            }

            return ExceptionSerializer::serializeException($e, $command);
        }
    }

    private static function getParseResponse(CommandInterface $command): CommandInterface
    {
        self::initializeHandlers();
        $response = self::$handlers[$command->getCommandType()->getValue()]->handleCommand($command);
        if (TypesHandler::isSimpleType($response)) {
            return Command::createResponse($response, $command->getRuntimeName());
        }

        if (self::isCommandGenerateLibType($response) || self::isCommandExceptionType($response)) {
            return $response;
        }

        if (is_array($response)) {
            $response = new ArrayWrapper($response);
        }

        return Command::createReference(
            ReferencesCache::getInstance()->cacheReference($response),
            $command->getRuntimeName()
        );
    }

    /**
     * @param mixed $result
     */
    private static function isCommandGenerateLibType($result): bool
    {
        if (is_object($result) && get_class($result) === Command::class) {
            return $result->getCommandType()->equalsByValue(CommandType::GENERATE_LIB);
        }

        return false;
    }

    /**
     * @param mixed $result
     */
    private static function isCommandExceptionType($result): bool
    {
        if (is_object($result) && get_class($result) === Command::class) {
            return $result->getCommandType()->equalsByValue(CommandType::EXCEPTION);
        }

        return false;
    }
}
