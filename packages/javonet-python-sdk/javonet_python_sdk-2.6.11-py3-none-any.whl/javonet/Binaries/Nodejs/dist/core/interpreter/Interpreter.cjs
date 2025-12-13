"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var Interpreter_exports = {};
__export(Interpreter_exports, {
  Interpreter: () => Interpreter
});
module.exports = __toCommonJS(Interpreter_exports);
var import_ConnectionType = require("../../utils/ConnectionType.cjs");
var import_Runtime = require("../../utils/Runtime.cjs");
var import_RuntimeName = require("../../utils/RuntimeName.cjs");
var import_CommandDeserializer = require("../protocol/CommandDeserializer.cjs");
var import_CommandSerializer = require("../protocol/CommandSerializer.cjs");
var import_TransmitterWebsocketBrowser = require("../transmitter/TransmitterWebsocketBrowser.cjs");
var import_TransmitterWebsocket = require("../transmitter/TransmitterWebsocket.cjs");
var import_Handler = require("../handler/Handler.cjs");
const import_meta = {};
let _Receiver;
let _Transmitter;
let _TransmitterWebsocket = (0, import_Runtime.isNodejsRuntime)() ? import_TransmitterWebsocket.TransmitterWebsocket : import_TransmitterWebsocketBrowser.TransmitterWebsocketBrowser;
const requireDynamic = (0, import_Runtime.getRequire)(import_meta.url);
class Interpreter {
  /**
   *
   * @param {Command} command
   * @param {IConnectionData} connectionData
   * @returns {Promise<Command>}
   */
  static async execute(command, connectionData) {
    try {
      let messageByteArray = import_CommandSerializer.CommandSerializer.serialize(command, connectionData);
      if (!(messageByteArray instanceof Uint8Array)) {
        throw new Error("Serialized message is not Uint8Array");
      }
      let responseByteArray = void 0;
      if (!(0, import_Runtime.isNodejsRuntime)() && connectionData.connectionType === import_ConnectionType.ConnectionType.IN_MEMORY) {
        throw new Error(
          "Nodejs Core Error: inMemory is only allowed in Nodejs runtime, not in browser"
        );
      }
      if (command.runtimeName === import_RuntimeName.RuntimeName.Nodejs && connectionData.connectionType === import_ConnectionType.ConnectionType.IN_MEMORY) {
        if (!_Receiver) {
          const { Receiver } = require("../receiver/Receiver.cjs");
          _Receiver = Receiver;
        }
        if (!_Receiver) {
          throw new Error("Nodejs Core Error: Receiver is undefined");
        }
        responseByteArray = await _Receiver.sendCommand(messageByteArray);
      } else if (connectionData.connectionType === import_ConnectionType.ConnectionType.IN_MEMORY || connectionData.connectionType === import_ConnectionType.ConnectionType.TCP) {
        if (!_Transmitter) {
          const { Transmitter } = require("../transmitter/Transmitter.cjs");
          _Transmitter = Transmitter;
        }
        if (!_Transmitter) {
          throw new Error("Nodejs Core Error: Transmitter is undefined");
        }
        responseByteArray = await _Transmitter.sendCommand(messageByteArray);
      } else if (connectionData.connectionType === import_ConnectionType.ConnectionType.WEB_SOCKET) {
        responseByteArray = await _TransmitterWebsocket.sendCommand(messageByteArray, connectionData);
      }
      if (!responseByteArray) {
        throw new Error("No response received from Transmitter");
      }
      return new import_CommandDeserializer.CommandDeserializer(responseByteArray).deserialize();
    } catch (error) {
      throw error;
    }
  }
  /**
   *
   * @param {Uint8Array} messageByteArray
   * @returns {Promise<Command> | Command}
   */
  static process(messageByteArray) {
    try {
      const receivedCommand = new import_CommandDeserializer.CommandDeserializer(messageByteArray).deserialize();
      return import_Handler.Handler.handleCommand(receivedCommand);
    } catch (error) {
      throw error;
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Interpreter
});
