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
var RegisterForUpdateHandler_exports = {};
__export(RegisterForUpdateHandler_exports, {
  RegisterForUpdateHandler: () => RegisterForUpdateHandler
});
module.exports = __toCommonJS(RegisterForUpdateHandler_exports);
var import_AbstractHandler = require("./AbstractHandler.cjs");
class RegisterForUpdateHandler extends import_AbstractHandler.AbstractHandler {
  requiredParametersCount = 2;
  /* type {Map<string, any>} */
  static _invocationContexts = { Value: /* @__PURE__ */ new Map() };
  /**
   * Ensure context map exists and return it.
   * @returns {Map<string, any>}
   */
  static getOrCreateContextMap() {
    const container = RegisterForUpdateHandler._invocationContexts;
    if (!container.Value) {
      container.Value = /* @__PURE__ */ new Map();
    }
    return container.Value;
  }
  /**
   * @param {any} command
   * @returns {any}
   */
  process(command) {
    if (command.payload.length < this.requiredParametersCount) {
      throw new Error("RegisterForUpdateHandler parameters mismatch");
    }
    const objectToRegister = command.payload[0];
    const guidToRegister = command.payload.length > 1 && typeof command.payload[1] === "string" ? command.payload[1] : "";
    const contextMap = RegisterForUpdateHandler.getOrCreateContextMap();
    if (!contextMap.has(guidToRegister)) {
      contextMap.set(guidToRegister, objectToRegister);
    }
    return objectToRegister;
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  RegisterForUpdateHandler
});
