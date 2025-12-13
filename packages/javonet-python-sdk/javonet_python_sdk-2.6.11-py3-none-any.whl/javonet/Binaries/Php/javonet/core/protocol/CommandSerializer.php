<?php

declare(strict_types=1);

namespace core\protocol;

use core\referencecache\ReferencesCache;
use Exception;
use RuntimeException;
use utils\Command;
use utils\CommandInterface;
use utils\connectiondata\IConnectionData;
use utils\RuntimeName;
use utils\type\CommandType;
use utils\TypesHandler;

final class CommandSerializer
{
    private const DEFAULT_SERIALIZER_CONNECTION_DATA = [0, 0, 0, 0, 0, 0, 0];

    private function __construct()
    {
    }

    /**
     * Serialize command to array of bytes (ints 0–255).
     *
     * @return int[]
     */
    public static function serialize(CommandInterface $rootCommand, ?IConnectionData $IConnectionData): array
    {
        try {
            $buffer = [];

            // Write runtime and version
            $buffer[] = $rootCommand->getRuntimeName()->getValue();
            $buffer[] = 0; // runtimeVersion

            // Write connection data
            self::insertIntoBuffer($buffer, self::getDataByIConnectionData($IConnectionData));

            // Write runtime name and command type header for PHP runtime
            self::insertIntoBuffer($buffer, [
                RuntimeName::PHP,
                $rootCommand->getCommandType()->getValue(),
            ]);

            // Serialize payload recursively
            self::serializeRecursively($rootCommand, $buffer);

            return $buffer;
        } catch (Exception $e) {
            throw new RuntimeException(
                'Error during serialization: ' . $e->getMessage(),
                0,
                $e
            );
        }
    }

    /**
     * @return int[]
     */
    private static function getDataByIConnectionData(?IConnectionData $IConnectionData): array
    {
        if ($IConnectionData !== null) {
            return $IConnectionData->serializeConnectionData();
        }

        return self::DEFAULT_SERIALIZER_CONNECTION_DATA;
    }

    /**
     * @param int[] $buffer
     * @param int[] $data
     */
    private static function insertIntoBuffer(array &$buffer, array $data): void
    {
        foreach ($data as $value) {
            $buffer[] = $value;
        }
    }

    /**
     * @param int[] $buffer
     */
    private static function serializeRecursively(CommandInterface $command, array &$buffer): void
    {
        foreach ($command->getPayload() as $payloadItem) {
            if ($payloadItem instanceof CommandInterface) {
                // Nested command
                self::insertIntoBuffer($buffer, TypeSerializer::serializeCommand($payloadItem));
                self::serializeRecursively($payloadItem, $buffer);
            } elseif (TypesHandler::isSimpleType($payloadItem)) {
                // Primitive or simple type
                self::insertIntoBuffer($buffer, TypeSerializer::serializePrimitive($payloadItem));
            } else {
                // Complex object – serialize as reference command
                $referenceId = ReferencesCache::getInstance()->cacheReference($payloadItem);

                $refCommand = new Command(
                    new RuntimeName(RuntimeName::PHP),
                    CommandType::REFERENCE(),
                    $referenceId
                );

                self::insertIntoBuffer($buffer, TypeSerializer::serializeCommand($refCommand));
                self::serializeRecursively($refCommand, $buffer);
            }
        }
    }
}
