# CHANGELOG

# 0.10.8 (2025-12-05)

### Improvements

- This PR introduces register reuse in Qpysequence. Registers can now be flagged as reusable in the code, allowing them to be reassigned once their usage in a block is complete.
This implementation effectively bypasses the Q1ASM limitation of 64 registers.
To enable this, a new attribute `reuse_registers` has been added to the Block class. Registers included in this list are automatically marked as available again once the block has finished execution. For Q1ASM readability, register allocation remains incremental and only falls back to previously used indices when more than 64 registers are required.
  [#68](https://github.com/qilimanjaro-tech/qpysequence/pull/68)


# 0.10.67 (2025-03-17)

### Bug fixes

- Relax numpy version to avoid 3rd party dependancies issues.
  [#66](https://github.com/qilimanjaro-tech/qpysequence/issues/66)

# 0.10.6 (2025-03-14)

### Improvements

- Convert some parameters in Sequence to optional.
  [#64](https://github.com/qilimanjaro-tech/qpysequence/pull/64)

# 0.10.5 (2024-12-17)

### Improvements

- Update versioning of publishing action. [#61](https://github.com/qilimanjaro-tech/qpysequence/pull/61)

- Updated dependency management and project building to `uv`.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

- Removed obsolete linting and formatting tools in favor of `ruff`.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

- Switched to `loguru` for logging.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

- Added `tox` and updated github actions to run tests against multiple python versions. `QpySequence` is now tested against python 3.10, 3.11, 3.12 and 3.13.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

- Updated tests to reach 100% coverage.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

### Documentation

- Removed broken documentation.
  [#62](https://github.com/qilimanjaro-tech/qpysequence/pull/62)

## 0.10.4 (2024-09-06)

### Improvements

- Improved `modify` and added tests.

[#59](https://github.com/qilimanjaro-tech/qpysequence/pull/59)

## 0.10.3 (2024-08-21)

### New features since last release

- Added `modify` and `modify_pair` inside waveforms to change the data of a waveform with an existing index. The function requires waveform name to apply the change.

[#57](https://github.com/qilimanjaro-tech/qpysequence/pull/57)

## 0.10.2 (2024-07-02)

### Improvements

- Changed the `Memory` interface to allow numbers to be re-used, in order to optimize registry allocation. Registers are now allocated and directly marked in-use with the method `allocate_register_and_mark_in_use(register)`, but can also be marked as out-of-use by calling `mark_out_of_use(register)`. This enables other registers that will be allocated later to use the same number.

  [#55](https://github.com/qilimanjaro-tech/qpysequence/pull/55)

## 0.10.1 (2024-03-11)

### New features since last release

- Introduced the `IterativeLoop` class, which facilitates the implementation of generic loops, accommodating negative values and parallelism.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Introduced the `InfiniteLoop` class, which facilitates the implementation of infinite loops.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

### Improvements

- Added the `label` and `comment` attributes to `Instruction`, and the `with_label` and `with_comment` methods to set them.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Refactored `__repr__` method of `Instruction` to take into account the `label` and `comment` attributes.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Refactored `__repr__` method of `Block` to remove padding from nested blocks.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

### Breaking changes

- This release targets systems which are using `qblox_instruments` with version `>=0.10.0` and clusters with firmware version `>=0.5.0`.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Altered the output formatting of Q1ASM programs. The functionality remains the same, but external tests depending on string equality might break.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

### Bug fixes

- Fix incorrect comparison for the minimum waiting time
  [#51](https://github.com/qilimanjaro-tech/qpysequence/issues/51)

- Modified the `is_immediate_valid` method to take into account negative values.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Corrected parameter naming in `SetAwgOffs` instruction.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Adjusted permissible ranges in `SetAwgGain`, `SetAwgOffs`, and `SetFreq` instructions.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Updated `library.set_freq_hz` method to calculate correct Hz to Q1ASM value for frequency.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Updated `library.set_awg_gain_relative` method to take into account the correct range of the gain.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Updated `Jmp` instruction to allow jumping to label.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

- Modified real-time operations to take into account the minimum duration, removing the previous check for multiples of 4.
  [#48](https://github.com/qilimanjaro-tech/qpysequence/pull/48)

## 0.9.3 (2023-09-08)

### Improvements

- Adapted latch instructions to modifications in firmware version 0.6.0.
  [#46](https://github.com/qilimanjaro-tech/qpysequence/pull/46)

## 0.9.2 (2023-07-21)

### Bug fixes

- Updated the version tag in the libary init
  [#44](https://github.com/qilimanjaro-tech/qpysequence/pull/44)

## 0.9.1 (2023-07-20)

### Improvements

- The `Sequence` components: `Program`, `Acquisition`, `Weights` and `Waveforms` can now be imported from the root package.
  [#42](https://github.com/qilimanjaro-tech/qpysequence/pull/42)

- The usage of generic typing hints from the library `typings` such as `List`, `Dict` and `Tuple` have been replaced by the standard `list`, `dict` and `tuple`.
  [#42](https://github.com/qilimanjaro-tech/qpysequence/pull/42)

- The out of bounds exception now includes the valid range in the error message.
  [#42](https://github.com/qilimanjaro-tech/qpysequence/pull/42)

### Breaking changes

- `Sequence` argument `weights` should now be an object of the `Weights` class, instead of a dictionary.
  [#42](https://github.com/qilimanjaro-tech/qpysequence/pull/42)

### Deprecations

- `Block.append_component()` and `Block.append_instruction()` have been made private. Now `Block.append_component()` should always be called to append a `Block` or `Instruction` to the `Block`.
  [#42](https://github.com/qilimanjaro-tech/qpysequence/pull/42)

### Documentation

### Bug fixes

## 0.9.0 (2023-05-12)

### New features since last release

- Added new ChangeLog!
  [#36](https://github.com/qilimanjaro-tech/qpysequence/pull/36)

- Support for all new Q1ASM instructions released for cluster firmware 0.4.0 (`qblox-instruments==0.9.0`).
  [#34](https://github.com/qilimanjaro-tech/qpysequence/pull/34)

### Improvements

- Existing and new instructions have been reorganized in packages following the same classification as in [Qblox Sequencer docs](https://qblox-qblox-instruments.readthedocs-hosted.com/en/master/documentation/sequencer.html).
  [#34](https://github.com/qilimanjaro-tech/qpysequence/pull/34)

### Breaking changes

### Deprecations

- `SwReq` instruction has been removed.
  [#34](https://github.com/qilimanjaro-tech/qpysequence/pull/34)

### Documentation

- Extended instruction docstrings to include information relevant to the RF modules.
  [#34](https://github.com/qilimanjaro-tech/qpysequence/pull/34)

### Bug fixes

## 0.8.0 (2023-02-17)

### Feat

- multiply function (#32)

## 0.7.0 (2023-02-15)

### Feat

- automatic nop instructions (#30)

## 0.6.1 (2023-01-18)

### Refactor

- one instruction class per module (#29)

## 0.6.0 (2023-01-18)

### Feat

- add Weights Class (#26)

## 0.5.0 (2023-01-17)

### Feat

- support qblox 0.8.1 (#25)

## 0.4.0 (2023-01-12)

### Feat

- builtin-components (#23)

## 0.3.2 (2022-10-20)

### Fix

- typo in instruction name

## 0.3.1 (2022-10-05)

### Fix

- loop reverse order and missing nop instructions

## 0.3.0 (2022-09-27)

### Feat

- flexible loops

## 0.2.0 (2022-09-23)

### Feat

- updates new register new version
- Change string registers to a Register class

### Refactor

- reorganize modules

## 0.1.0 (2022-05-08)

### Feat

- Implement new sequencer (#1)

## 0.0.0 (2022-04-07)
