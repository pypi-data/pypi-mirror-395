export class Receiver {
    static connectionData: InMemoryConnectionData;
    static getRuntimeInfo(): string;
    /**
     * @param {Uint8Array} messageByteArray
     * @returns {Promise<Uint8Array>}
     */
    static sendCommand(messageByteArray: Uint8Array): Promise<Uint8Array>;
    /**
     * @param {Uint8Array} messageByteArray
     * @returns {Promise<Uint8Array>}
     */
    static heartBeat(messageByteArray: Uint8Array): Promise<Uint8Array>;
}
import { InMemoryConnectionData } from '../../utils/connectionData/InMemoryConnectionData.js';
