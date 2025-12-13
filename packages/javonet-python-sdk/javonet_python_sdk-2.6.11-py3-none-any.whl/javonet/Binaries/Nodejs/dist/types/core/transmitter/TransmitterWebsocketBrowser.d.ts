/**
 * @typedef {import('../../utils/connectionData/IConnectionData.js').IConnectionData} IConnectionData
 */
export class TransmitterWebsocketBrowser {
    /**
     * @returns {void}
     */
    static initialize(): void;
    /**
     * @returns {void}
     */
    static activate(): void;
    /**
     * @async
     * @param {Uint8Array} messageByteArray
     * @param {IConnectionData} connectionData
     * @returns {Promise<Uint8Array>} responseByteArray
     */
    static sendCommand(messageByteArray: Uint8Array, connectionData: IConnectionData): Promise<Uint8Array>;
    /**
     * @async
     * @param {any} configSource
     * @returns {void}
     */
    static setConfigSource(configSource: any): void;
}
export type IConnectionData = import("../../utils/connectionData/IConnectionData.js").IConnectionData;
