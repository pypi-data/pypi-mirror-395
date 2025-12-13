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
var ComplexTypeResolver_exports = {};
__export(ComplexTypeResolver_exports, {
  ComplexTypeResolver: () => ComplexTypeResolver
});
module.exports = __toCommonJS(ComplexTypeResolver_exports);
var import_Primitives = require("../../utils/Primitives.cjs");
var import_Runtime = require("../../utils/Runtime.cjs");
var import_RuntimeName = require("../../utils/RuntimeName.cjs");
var import_Activator = require("../Activator.cjs");
var import_ActivatorDetails = require("../ActivatorDetails.cjs");
var import_InvocationContext = require("../InvocationContext.cjs");
var import_JavaTypeParsingFunctions = require("./typeParsingFunctions/JavaTypeParsingFunctions.cjs");
var import_NetcoreTypeParsingFunctions = require("./typeParsingFunctions/NetcoreTypeParsingFunctions.cjs");
var import_NodejsTypeParsingFunctions = require("./typeParsingFunctions/NodejsTypeParsingFunctions.cjs");
var import_PythonTypeParsingFunctions = require("./typeParsingFunctions/PythonTypeParsingFunctions.cjs");
const import_meta = {};
const dynamicImport = (0, import_Runtime.getRequire)(import_meta.url);
const typeParsingFunctions = /* @__PURE__ */ new Map([
  [import_RuntimeName.RuntimeName.Netcore, import_NetcoreTypeParsingFunctions.NetcoreTypeParsingFunctions],
  [import_RuntimeName.RuntimeName.Jvm, import_JavaTypeParsingFunctions.JavaTypeParsingFunctions],
  [import_RuntimeName.RuntimeName.Nodejs, import_NodejsTypeParsingFunctions.NodejsTypeParsingFunctions],
  [import_RuntimeName.RuntimeName.Python, import_PythonTypeParsingFunctions.PythonTypeParsingFunctions],
  [import_RuntimeName.RuntimeName.Python27, import_PythonTypeParsingFunctions.PythonTypeParsingFunctions]
]);
class ComplexTypeResolver {
  /** @type {Map<string, ActivatorDetails>} */
  #typeMap;
  constructor() {
    this.#typeMap = /* @__PURE__ */ new Map();
  }
  /**
   * Register a custom type mapping
   * @param {string} resultType - The type name from the target runtime
   * @param {Function} type - The JavaScript constructor function
   * @param {any[]} [args] - Default arguments for the constructor
   */
  register(resultType, type, args) {
    if (!this.#typeMap.has(resultType)) {
      this.#typeMap.set(resultType, new import_ActivatorDetails.ActivatorDetails(type, args));
    }
  }
  /**
   * Convert InvocationContext result to appropriate JavaScript type
   * @param {InvocationContext} ic - The invocation context
   * @returns {Promise<any>} The converted result
   */
  async convertResult(ic) {
    const runtimeName = ic.getRuntimeName();
    const resultType = await ic.getResultType();
    if (!resultType) {
      throw new Error("resultType is not valid");
    }
    let underlyingType = ComplexTypeResolver.tryGetUnderlyingArrayType(resultType);
    if (underlyingType !== null) {
      const { Type } = (
        /** @type {ActivatorDetails} */
        this.#typeMap.get(underlyingType)
      );
      const complexTypesArray = await ic.retrieveArray();
      return complexTypesArray.map((item) => import_Activator.Activator.createInstance(Type, item));
    }
    const parsingFunction = ComplexTypeResolver.tryGetTypeParsingFunction(runtimeName, resultType);
    if (parsingFunction) {
      return parsingFunction(ic);
    }
    const activatorDetails = this.tryGetValueFromTypeMap(resultType);
    if (!activatorDetails) {
      throw new Error(`No type registered for key '${resultType}'.`);
    }
    if (runtimeName === import_RuntimeName.RuntimeName.Nodejs) {
      const value = await ic.getValue();
      if (value) {
        if (value instanceof activatorDetails.Type) {
          return value;
        }
      }
    }
    return import_Activator.Activator.createInstance(activatorDetails.Type, activatorDetails.arguments ?? null);
  }
  /**
   * Resolve type from string name and optional module
   * @param {string} typeName - Name of the type to resolve
   * @param {string} [moduleName] - Optional module name to import from
   * @returns {Function} The resolved type/constructor function
   */
  static resolveType(typeName, moduleName) {
    if (moduleName) {
      try {
        const module2 = dynamicImport(moduleName);
        const typeObj2 = module2[typeName];
        if (!typeObj2) {
          throw new Error(`Type '${typeName}' not found in module '${moduleName}'`);
        }
        return typeObj2;
      } catch (error) {
        throw new Error(
          `Failed to resolve type '${typeName}' from module '${moduleName}': ${/** @type {Error} */
          error.message}`
        );
      }
    }
    const globalScope = typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : {};
    const typeObj = (
      /** @type {Record<string, any>} */
      globalScope[typeName]
    );
    if (!typeObj) {
      throw new Error(`Type '${typeName}' not found in global scope`);
    }
    return typeObj;
  }
  /**
   * Attempts to extract the underlying element type from an array type string
   * @param {string} type - The type string to parse (e.g., "MyType[]")
   * @returns {string | null} Object indicating success and the element type
   * @throws {Error} If the array element type is a primitive type
   */
  static tryGetUnderlyingArrayType(type) {
    if (typeof type !== "string" || !type.includes("[")) {
      return null;
    }
    let trimmedType = type.trim();
    if (!trimmedType) return null;
    const commaIndex = trimmedType.indexOf(",");
    if (commaIndex > 0) {
      trimmedType = trimmedType.substring(0, commaIndex).trim();
    }
    const bracketIndex = trimmedType.indexOf("[");
    if (bracketIndex > 0) {
      trimmedType = trimmedType.substring(0, bracketIndex).trim();
    }
    if (import_Primitives.PrimitiveSet.has(trimmedType)) {
      throw new Error("Primitive array element types are not supported.");
    }
    return trimmedType;
  }
  /**
   * @param {RuntimeName} runtimeName
   * @param {string} resultType
   * @returns {any}
   */
  static tryGetTypeParsingFunction(runtimeName, resultType) {
    const runtimeDict = typeParsingFunctions.get(runtimeName);
    return runtimeDict ? runtimeDict.get(resultType) ?? null : null;
  }
  /**
   * @param {string} resultType
   * @returns {ActivatorDetails | null}
   */
  tryGetValueFromTypeMap(resultType) {
    if (!resultType) {
      throw new Error("resultType is not valid");
    }
    return this.#typeMap.get(resultType) ?? null;
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ComplexTypeResolver
});
