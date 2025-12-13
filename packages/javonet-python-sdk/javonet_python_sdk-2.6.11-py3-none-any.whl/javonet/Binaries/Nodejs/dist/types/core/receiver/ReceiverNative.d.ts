export class ReceiverNative {
    /**
     * @param {Uint8Array} messageByteArray
     * @returns {Promise<Uint8Array> | Uint8Array}
     */
    static sendCommand(messageByteArray: Uint8Array): Promise<Uint8Array> | Uint8Array;
    /**
     * @param {Uint8Array} messageByteArray
     * @returns {Uint8Array | Promise<Uint8Array>}
     */
    static heartBeat(messageByteArray: Uint8Array): Uint8Array | Promise<Uint8Array>;
}
