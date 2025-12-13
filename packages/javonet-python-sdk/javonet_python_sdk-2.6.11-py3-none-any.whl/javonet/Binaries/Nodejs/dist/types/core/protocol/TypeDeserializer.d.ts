export class TypeDeserializer {
    /**
     * @param {Uint8Array} encodedCommand
     * @returns {Command}
     */
    static deserializeCommand(encodedCommand: Uint8Array): Command;
    /**
     * @param {number} stringEncodingMode
     * @param {Uint8Array} encodedString
     */
    static deserializeString(stringEncodingMode: number, encodedString: Uint8Array): string;
    /**
     * @param {Uint8Array} encodedInt
     */
    static deserializeInt(encodedInt: Uint8Array): number;
    /**
     * @param {Uint8Array} encodedBool
     */
    static deserializeBool(encodedBool: Uint8Array): boolean;
    /**
     * @param {Uint8Array} encodedFloat
     */
    static deserializeFloat(encodedFloat: Uint8Array): number;
    /**
     * @param {Uint8Array} encodedByte
     */
    static deserializeByte(encodedByte: Uint8Array): number;
    /**
     * @param {Uint8Array} encodedChar
     */
    static deserializeChar(encodedChar: Uint8Array): number;
    /**
     * @param {Uint8Array} encodedLongLong
     */
    static deserializeLongLong(encodedLongLong: Uint8Array): bigint;
    /**
     * @param {Uint8Array} encodedDouble
     */
    static deserializeDouble(encodedDouble: Uint8Array): number;
    /**
     * @param {Uint8Array} encodedULLong
     */
    static deserializeULLong(encodedULLong: Uint8Array): bigint;
    /**
     * @param {Uint8Array} encodedUInt
     */
    static deserializeUInt(encodedUInt: Uint8Array): number;
    static deserializeNull(encodedNull?: null): null;
}
import { Command } from '../../utils/Command.js';
