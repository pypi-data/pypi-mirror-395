/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* TypeDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_TYPEDEF_LIST
#undef GET_TYPEDEF_LIST

::mlir::amdgpu::TDMBaseType,
::mlir::amdgpu::TDMDescriptorType

#endif // GET_TYPEDEF_LIST

#ifdef GET_TYPEDEF_CLASSES
#undef GET_TYPEDEF_CLASSES

static ::mlir::OptionalParseResult generatedTypeParser(::mlir::AsmParser &parser, ::llvm::StringRef *mnemonic, ::mlir::Type &value) {
  return ::mlir::AsmParser::KeywordSwitch<::mlir::OptionalParseResult>(parser)
    .Case(::mlir::amdgpu::TDMBaseType::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::amdgpu::TDMBaseType::parse(parser);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::amdgpu::TDMDescriptorType::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::amdgpu::TDMDescriptorType::get(parser.getContext());
      return ::mlir::success(!!value);
    })
    .Default([&](llvm::StringRef keyword, llvm::SMLoc) {
      *mnemonic = keyword;
      return std::nullopt;
    });
}

static ::llvm::LogicalResult generatedTypePrinter(::mlir::Type def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Type, ::llvm::LogicalResult>(def)    .Case<::mlir::amdgpu::TDMBaseType>([&](auto t) {
      printer << ::mlir::amdgpu::TDMBaseType::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::amdgpu::TDMDescriptorType>([&](auto t) {
      printer << ::mlir::amdgpu::TDMDescriptorType::getMnemonic();
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir::amdgpu {

namespace detail {

struct TDMBaseTypeStorage : public ::mlir::TypeStorage {
  using KeyTy = std::tuple<Type>;
  TDMBaseTypeStorage(Type elementType) : elementType(std::move(elementType)) {}

  KeyTy getAsKey() const {
    return KeyTy(elementType);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (elementType == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static TDMBaseTypeStorage *construct(::mlir::TypeStorageAllocator &allocator, KeyTy &&tblgenKey) {
    auto elementType = std::move(std::get<0>(tblgenKey));
    return new (allocator.allocate<TDMBaseTypeStorage>()) TDMBaseTypeStorage(std::move(elementType));
  }

  Type elementType;
};

} // namespace detail
TDMBaseType TDMBaseType::get(::mlir::MLIRContext *context, Type elementType) {
  return Base::get(context, std::move(elementType));
}

TDMBaseType TDMBaseType::get(Type elementType) {
  return Base::get(elementType.getContext(), elementType);
}

::mlir::Type TDMBaseType::parse(::mlir::AsmParser &odsParser) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<Type> _result_elementType;
  // Parse literal '<'
  if (odsParser.parseLess()) return {};

  // Parse variable 'elementType'
  _result_elementType = ::mlir::FieldParser<Type>::parse(odsParser);
  if (::mlir::failed(_result_elementType)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse AMDGPU_TDMBaseType parameter 'elementType' which is to be a `Type`");
    return {};
  }
  // Parse literal '>'
  if (odsParser.parseGreater()) return {};
  assert(::mlir::succeeded(_result_elementType));
  return TDMBaseType::get(odsParser.getContext(),
      Type((*_result_elementType)));
}

void TDMBaseType::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << "<";
  odsPrinter.printStrippedAttrOrType(getElementType());
  odsPrinter << ">";
}

Type TDMBaseType::getElementType() const {
  return getImpl()->elementType;
}


} // namespace mlir::amdgpu
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::amdgpu::TDMBaseType)
namespace mlir::amdgpu {


} // namespace mlir::amdgpu
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::amdgpu::TDMDescriptorType)
namespace mlir::amdgpu {


/// Parse a type registered to this dialect.
::mlir::Type AMDGPUDialect::parseType(::mlir::DialectAsmParser &parser) const {
  ::llvm::SMLoc typeLoc = parser.getCurrentLocation();
  ::llvm::StringRef mnemonic;
  ::mlir::Type genType;
  auto parseResult = generatedTypeParser(parser, &mnemonic, genType);
  if (parseResult.has_value())
    return genType;
  
  parser.emitError(typeLoc) << "unknown  type `"
      << mnemonic << "` in dialect `" << getNamespace() << "`";
  return {};
}
/// Print a type registered to this dialect.
void AMDGPUDialect::printType(::mlir::Type type,
                    ::mlir::DialectAsmPrinter &printer) const {
  if (::mlir::succeeded(generatedTypePrinter(type, printer)))
    return;
  
}

} // namespace mlir::amdgpu

#endif // GET_TYPEDEF_CLASSES

