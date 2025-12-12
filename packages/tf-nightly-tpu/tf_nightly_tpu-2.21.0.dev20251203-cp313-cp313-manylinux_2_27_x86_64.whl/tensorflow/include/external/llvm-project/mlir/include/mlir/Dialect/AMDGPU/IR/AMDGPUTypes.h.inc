/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* TypeDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_TYPEDEF_CLASSES
#undef GET_TYPEDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir::amdgpu {

/// Pair of base addresses that move data between LDS and global storage.
/// This type is opaque and it is used to represent a struct of two addresses.
///     One address is in LDS while the other is in global memory.
class TDMBaseType;
namespace detail {

struct TDMBaseTypeStorage;

} // namespace detail
class TDMBaseType : public ::mlir::Type::TypeBase<TDMBaseType, ::mlir::Type, detail::TDMBaseTypeStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "amdgpu.tdm_base";
  static constexpr ::llvm::StringLiteral dialectName = "amdgpu";
  static TDMBaseType get(::mlir::MLIRContext *context, Type elementType);
  static TDMBaseType get(Type elementType);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"tdm_base"};
  }

  static ::mlir::Type parse(::mlir::AsmParser &odsParser);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  Type getElementType() const;
};

} // namespace mlir::amdgpu
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::amdgpu::TDMBaseType)

#endif // GET_TYPEDEF_CLASSES

