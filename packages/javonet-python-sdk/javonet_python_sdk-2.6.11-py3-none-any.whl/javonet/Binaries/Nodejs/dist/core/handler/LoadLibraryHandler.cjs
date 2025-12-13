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
var LoadLibraryHandler_exports = {};
__export(LoadLibraryHandler_exports, {
  LoadLibraryHandler: () => LoadLibraryHandler
});
module.exports = __toCommonJS(LoadLibraryHandler_exports);
var import_Runtime = require("../../utils/Runtime.cjs");
var import_AbstractHandler = require("./AbstractHandler.cjs");
const import_meta = {};
let _existsSync = null;
let _resolve = null;
const requireDynamic = (0, import_Runtime.getRequire)(import_meta.url);
class LoadLibraryHandler extends import_AbstractHandler.AbstractHandler {
  requiredParametersCount = 1;
  /** @type {string[]} */
  static loadedLibraries = [];
  constructor() {
    super();
  }
  /**
   * @param {Command} command
   */
  process(command) {
    if (command.payload.length < this.requiredParametersCount) {
      throw new Error("Load Library parameters mismatch");
    }
    const { payload } = command;
    const [lib] = payload;
    if (!lib) {
      throw new Error("Cannot load module: Library path is required but was not provided");
    }
    if (!_existsSync) {
      const { existsSync } = requireDynamic("fs");
      _existsSync = existsSync;
    }
    if (!_resolve) {
      const { resolve } = requireDynamic("path");
      _resolve = resolve;
    }
    const absolutePath = _resolve ? _resolve(lib) : lib;
    const candidatePaths = [lib, absolutePath];
    const existingPath = candidatePaths.find((p) => _existsSync && _existsSync(p));
    if (!existingPath) {
      throw new Error(`Cannot load module: Library not found: ${lib}`);
    }
    const normalizedPath = _resolve ? _resolve(existingPath) : existingPath;
    if (LoadLibraryHandler.loadedLibraries.includes(normalizedPath)) {
      return 0;
    }
    const pathArray = normalizedPath.split(/[/\\]/);
    let libraryName = pathArray.length > 1 ? pathArray[pathArray.length - 1] : pathArray[0];
    libraryName = libraryName.replace(/\.js$/i, "");
    let moduleExports;
    try {
      moduleExports = requireDynamic(normalizedPath);
      LoadLibraryHandler.loadedLibraries.push(normalizedPath);
    } catch (error) {
      throw new Error("Cannot load module: " + normalizedPath + "\n" + error);
    }
    global[libraryName] = moduleExports;
    for (const [key, value] of Object.entries(moduleExports)) {
      global[key] = value;
    }
    return 0;
  }
  getLoadedLibraries() {
    return LoadLibraryHandler.loadedLibraries;
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  LoadLibraryHandler
});
