// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Fri Dec 5 12:44:58 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "2202e2a5";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.19";
  return version;
}

}  // namespace sherpa_onnx
