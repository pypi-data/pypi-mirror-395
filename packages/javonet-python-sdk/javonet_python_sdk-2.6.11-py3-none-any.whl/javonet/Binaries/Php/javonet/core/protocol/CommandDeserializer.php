<?php

declare(strict_types=1);

namespace core\protocol;

use utils\Command;
use utils\CommandInterface;
use utils\exception\TypeByteNotSupportedException;
use utils\RuntimeName;
use utils\StringEncodingMode;
use utils\type\CommandType;
use utils\type\JType;

final class CommandDeserializer
{
    private function __construct()
    {
    }

    /**
     * @param int[] $buffer
     */
    public static function deserialize(array $buffer): CommandInterface
    {
        $position = 11;
        $bufferLength = count($buffer);

        $runtimeName = new RuntimeName($buffer[0]);
        $commandType = new CommandType($buffer[10]);
        $payload = [];

        while ($position < $bufferLength) {
            $payload[] = self::readObject($buffer, $position);
        }

        // Single Command instance created once with full payload
        return new Command($runtimeName, $commandType, $payload);
    }

    /**
     * @param int[] $buffer
     * @return mixed
     */
    private static function readObject(array $buffer, int &$position)
    {
        $typeByte = new JType($buffer[$position]);

        switch ($typeByte->getValue()) {
            case JType::JAVONET_COMMAND:
                return self::readCommand($buffer, $position);
            case JType::JAVONET_STRING:
                return self::readString($buffer, $position);
            case JType::JAVONET_INTEGER:
                return self::readInt($buffer, $position);
            case JType::JAVONET_BOOLEAN:
                return self::readBool($buffer, $position);
            case JType::JAVONET_FLOAT:
                return self::readFloat($buffer, $position);
            case JType::JAVONET_BYTE:
                return self::readByte($buffer, $position);
            case JType::JAVONET_CHAR:
                return self::readChar($buffer, $position);
            case JType::JAVONET_LONG:
                return self::readLong($buffer, $position);
            case JType::JAVONET_DOUBLE:
                return self::readDouble($buffer, $position);
            case JType::JAVONET_UNSIGNED_LONG_LONG:
                return self::readUnsignedLong($buffer, $position);
            case JType::JAVONET_UNSIGNED_INTEGER:
                return self::readUnsignedInteger($buffer, $position);
            case JType::JAVONET_NULL:
                return self::readNull($buffer, $position);
            default:
                throw new TypeByteNotSupportedException($buffer[$position]);
        }
    }

    /**
     * @param int[] $buffer
     */
    protected static function readCommand(array $buffer, int &$position): CommandInterface
    {
        $p = $position;

        $numberOfElementsInPayload = TypeDeserializer::deserializeInt([
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
            $buffer[$p + 4],
        ]);

        $runtime     = $buffer[$p + 5];
        $commandType = $buffer[$p + 6];

        $position += 7;

        $payload = [];
        for ($i = 0; $i < $numberOfElementsInPayload; $i++) {
            $payload[$i] = self::readObject($buffer, $position);
        }

        return new Command(
            new RuntimeName($runtime),
            new CommandType($commandType),
            $payload
        );
    }

    /**
     * @param int[] $buffer
     */
    private static function readString(array $buffer, int &$position): string
    {
        $p = $position;

        $stringEncodingMode = new StringEncodingMode($buffer[$p + 1]);

        $size = TypeDeserializer::deserializeInt([
            $buffer[$p + 2],
            $buffer[$p + 3],
            $buffer[$p + 4],
            $buffer[$p + 5],
        ]);

        $position += 6;
        $p = $position;
        $position += $size;

        // For strings, size can be large, so array_slice is acceptable here.
        $bytes = array_slice($buffer, $p, $size);

        return TypeDeserializer::deserializeString($stringEncodingMode, $bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readInt(array $buffer, int &$position): int
    {
        $size = 4;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
        ];

        return TypeDeserializer::deserializeInt($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readBool(array $buffer, int &$position): bool
    {
        $size = 1;
        $position += 2;
        $p = $position;
        $position += $size;

        // Keep passing array to match existing TypeDeserializer signature
        $bytes = [$buffer[$p]];

        return TypeDeserializer::deserializeBool($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readFloat(array $buffer, int &$position): float
    {
        $size = 4;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
        ];

        return TypeDeserializer::deserializeFloat($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readByte(array $buffer, int &$position): int
    {
        $size = 1;
        $position += 2;
        $p = $position;
        $position += $size;

        return TypeDeserializer::deserializeByte($buffer[$p]);
    }

    /**
     * @param int[] $buffer
     */
    private static function readChar(array $buffer, int &$position): string
    {
        $size = 1;
        $position += 2;
        $p = $position;
        $position += $size;

        return TypeDeserializer::deserializeChar($buffer[$p]);
    }

    /**
     * @param int[] $buffer
     */
    private static function readLong(array $buffer, int &$position): int
    {
        $size = 8;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
            $buffer[$p + 4],
            $buffer[$p + 5],
            $buffer[$p + 6],
            $buffer[$p + 7],
        ];

        return TypeDeserializer::deserializeLong($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readDouble(array $buffer, int &$position): float
    {
        $size = 8;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
            $buffer[$p + 4],
            $buffer[$p + 5],
            $buffer[$p + 6],
            $buffer[$p + 7],
        ];

        return TypeDeserializer::deserializeDouble($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readUnsignedLong(array $buffer, int &$position): int
    {
        $size = 8;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
            $buffer[$p + 4],
            $buffer[$p + 5],
            $buffer[$p + 6],
            $buffer[$p + 7],
        ];

        return TypeDeserializer::deserializeLong($bytes);
    }

    /**
     * @param int[] $buffer
     */
    private static function readUnsignedInteger(array $buffer, int &$position): int
    {
        $size = 4;
        $position += 2;
        $p = $position;
        $position += $size;

        $bytes = [
            $buffer[$p],
            $buffer[$p + 1],
            $buffer[$p + 2],
            $buffer[$p + 3],
        ];

        return TypeDeserializer::deserializeInt($bytes);
    }

    /**
     * @param int[] $buffer
     * @return mixed
     */
    private static function readNull(array $buffer, int &$position)
    {
        $size = 1;
        $position += 2;
        $position += $size;

        // Current TypeDeserializer::deserializeNull() in your PHP version
        // takes no args; keep that behavior.
        return TypeDeserializer::deserializeNull();
    }
}
