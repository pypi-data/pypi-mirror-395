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
var ConfigSourceResolver_exports = {};
__export(ConfigSourceResolver_exports, {
  ConfigSourceResolver: () => ConfigSourceResolver
});
module.exports = __toCommonJS(ConfigSourceResolver_exports);
var import_ConfigsDictionary = require("./ConfigsDictionary.cjs");
var import_JsonConfigResolver = require("./configResolvers/JsonConfigResolver.cjs");
var import_YamlConfigResolver = require("./configResolvers/YamlConfigResolver.cjs");
var import_ConnectionStringConfigResolver = require("./configResolvers/ConnectionStringConfigResolver.cjs");
var import_Runtime = require("../../utils/Runtime.cjs");
const import_meta = {};
let fs = null;
let process = null;
const requireDynamic = (0, import_Runtime.getRequire)(import_meta.url);
class ConfigSourceResolver {
  /**
   * @param {import('./ConfigPriority.js').ConfigPriority} priority
   * @param {string | any} configSource
   */
  static addConfigs(priority, configSource) {
    console.log(`Adding config from source: ${configSource} with priority '${priority}'`);
    if (configSource && typeof configSource === "object") {
      import_JsonConfigResolver.JsonConfigResolver.addConfigs(priority, configSource);
    } else {
      const configString = ConfigSourceResolver._getConfigSourceAsString(configSource);
      ConfigSourceResolver._parseConfigsAndAddToCollection(priority, configString);
    }
  }
  /**
   * @param {string} configName
   * @returns {*}
   */
  static getConfig(configName) {
    console.log(`Retrieving config ${configName}`);
    return import_ConfigsDictionary.ConfigsDictionary.getConfig(configName);
  }
  static clearConfigs() {
    import_ConfigsDictionary.ConfigsDictionary.clearConfigs();
  }
  /**
   * @param {string} configSource
   * @returns {string}
   */
  static _getConfigSourceAsString(configSource) {
    if (!configSource || configSource.trim() === "") {
      throw new Error("Config source cannot be null or whitespace.");
    }
    if ((0, import_Runtime.isNodejsRuntime)()) {
      if (!process) {
        process = requireDynamic("process");
      }
      if (!fs) {
        fs = requireDynamic("fs");
      }
      const envValue = process?.env[configSource];
      if (envValue && envValue.trim() !== "") {
        configSource = envValue;
      }
      if (fs?.existsSync(configSource) && fs?.statSync(configSource).isFile()) {
        configSource = fs.readFileSync(configSource, { encoding: "utf-8" });
      }
    }
    return configSource.trim();
  }
  /**
   * @param {import('./ConfigPriority.js').ConfigPriority} priority
   * @param {string} configString
   * @returns
   */
  static _parseConfigsAndAddToCollection(priority, configString) {
    try {
      const jsonObject = JSON.parse(configString);
      import_JsonConfigResolver.JsonConfigResolver.addConfigs(priority, jsonObject);
      return;
    } catch (ex) {
      if (ex instanceof SyntaxError) {
      } else {
        console.log("Failed to parse config source as JSON: " + ex);
      }
    }
    try {
      import_YamlConfigResolver.YamlConfigResolver.addConfigs(priority, configString);
      return;
    } catch (ex) {
      if (ex?.name === "SyntaxError") {
      } else {
        console.log("Failed to parse config source as YAML: " + ex);
      }
    }
    try {
      import_ConnectionStringConfigResolver.ConnectionStringConfigResolver.addConfigs(priority, configString);
      return;
    } catch (ex) {
      console.log("Failed to parse config source as connection string: " + ex);
    }
    throw new Error(
      "Config source is not valid JSON, YAML, or connection string format:\n" + configString
    );
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ConfigSourceResolver
});
