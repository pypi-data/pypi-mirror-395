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
var ActivatorDetails_exports = {};
__export(ActivatorDetails_exports, {
  ActivatorDetails: () => ActivatorDetails
});
module.exports = __toCommonJS(ActivatorDetails_exports);
class ActivatorDetails {
  /** @type {Function} */
  Type;
  /** @type {any[]} */
  arguments;
  /**
   * @param {Function} type - The constructor function/class
   * @param {any[]|any} [args] - Arguments to pass to constructor (array or single value)
   */
  constructor(type, args = []) {
    this.Type = type;
    if (args == null) {
      this.arguments = [];
    } else if (Array.isArray(args)) {
      this.arguments = args;
    } else {
      this.arguments = [args];
    }
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ActivatorDetails
});
