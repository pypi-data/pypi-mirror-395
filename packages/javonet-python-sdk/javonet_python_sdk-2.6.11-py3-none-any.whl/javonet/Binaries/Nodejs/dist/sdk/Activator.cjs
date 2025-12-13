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
var Activator_exports = {};
__export(Activator_exports, {
  Activator: () => Activator
});
module.exports = __toCommonJS(Activator_exports);
class Activator {
  /**
   * Create a new instance of a type
   * @param {Function} Type - The constructor function/class
   * @param {any[] | any} args - The arguments to pass to the constructor
   * @returns {any} The new instance
   */
  static createInstance(Type, args) {
    if (args == null) {
      args = [];
    }
    if (!Array.isArray(args)) {
      args = [args];
    }
    return new Type(...args);
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Activator
});
