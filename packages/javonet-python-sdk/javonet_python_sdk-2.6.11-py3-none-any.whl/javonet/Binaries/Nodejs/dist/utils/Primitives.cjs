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
var Primitives_exports = {};
__export(Primitives_exports, {
  PrimitiveSet: () => PrimitiveSet
});
module.exports = __toCommonJS(Primitives_exports);
const PrimitiveSet = new Set(
  [
    // --- JavaScript / TypeScript ---
    "string",
    "number",
    "boolean",
    "bigint",
    "symbol",
    "undefined",
    "null",
    // --- .NET / C# ---
    "bool",
    "boolean",
    "byte",
    "sbyte",
    "char",
    "decimal",
    "double",
    "float",
    "single",
    "int",
    "int32",
    "uint",
    "uint32",
    "long",
    "int64",
    "ulong",
    "uint64",
    "short",
    "int16",
    "ushort",
    "uint16",
    "object",
    "string",
    "system.boolean",
    "system.byte",
    "system.sbyte",
    "system.char",
    "system.decimal",
    "system.double",
    "system.single",
    "system.int",
    "system.int32",
    "system.uint",
    "system.uint32",
    "system.int64",
    "system.uint64",
    "system.int16",
    "system.uint16",
    "system.object",
    "system.string",
    // --- Java ---
    "byte",
    "short",
    "int",
    "long",
    "float",
    "double",
    "char",
    "boolean",
    "java.lang.string",
    // --- Python ---
    "str",
    "int",
    "float",
    "bool",
    "bytes",
    "bytearray",
    // --- Go ---
    "rune",
    "byte",
    "bool",
    "string",
    "int",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "float32",
    "float64",
    // --- C / C++ ---
    "char",
    "short",
    "int",
    "long",
    "float",
    "double",
    "signed char",
    "unsigned char",
    "unsigned short",
    "unsigned int",
    "unsigned long",
    // --- Rust ---
    "bool",
    "u8",
    "i8",
    "u16",
    "i16",
    "u32",
    "i32",
    "u64",
    "i64",
    "f32",
    "f64",
    "usize",
    "isize",
    "str",
    // --- Kotlin ---
    "boolean",
    "byte",
    "short",
    "int",
    "long",
    "float",
    "double",
    "char",
    "string",
    // --- Swift ---
    "bool",
    "int",
    "uint",
    "float",
    "double",
    "string",
    "character",
    // --- PHP ---
    "int",
    "integer",
    "float",
    "double",
    "string",
    "bool",
    "boolean",
    "mixed",
    // --- Ruby ---
    "string",
    "integer",
    "fixnum",
    "float",
    "symbol",
    "boolean",
    // --- Dart ---
    "int",
    "double",
    "num",
    "bool",
    "string",
    // --- Scala ---
    "int",
    "long",
    "double",
    "float",
    "char",
    "boolean",
    "string",
    // --- Haskell ---
    "int",
    "float",
    "double",
    "char",
    "bool",
    "integer",
    // --- Generic aliases ---
    "text",
    "primitive",
    "any",
    "void"
  ].map((x) => x.toLowerCase())
);
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  PrimitiveSet
});
