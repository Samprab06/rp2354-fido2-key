cmake_minimum_required(VERSION 3.13)

set(USB_VID 0x2E8A)
set(USB_PID 0x10FE)

# Hardcode target for RP2354 board (which uses rp2350 target in pico-sdk)
set(PICO_BOARD rp2350)
set(PICO_USE_FASTEST_SUPPORTED_CLOCK 1)

include(pico_sdk_import.cmake)

project(rp2354_fido2_key C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_executable(rp2354_fido2_key)

include(pico-keys-sdk/cmake/options.cmake)

option(ENABLE_POWER_ON_RESET "Enable/disable power cycle on reset" ON)
configure_bool_option(ENABLE_POWER_ON_RESET ENABLE_POWER_ON_RESET "Power cycle on reset: \t enabled" "Power cycle on reset: \t disabled")

option(ENABLE_OATH_APP "Enable/disable OATH application" ON)
configure_bool_option(ENABLE_OATH_APP ENABLE_OATH_APP "OATH Application: \t\t enabled" "OATH Application: \t\t disabled")

option(ENABLE_OTP_APP "Enable/disable OTP application" ON)
configure_bool_option(ENABLE_OTP_APP ENABLE_OTP_APP "OTP Application: \t\t enabled" "OTP Application: \t\t disabled")

if(FORBID_DISABLE_AUV)
    add_compile_definitions(FORBID_DISABLE_AUV=1)
endif()
if(DEFAULT_MCUV_NOT_REQUIRED)
    add_compile_definitions(DEFAULT_MCUV_NOT_REQUIRED=1)
endif()
if(DEFAULT_PIN_POLICY)
    add_compile_definitions(DEFAULT_PIN_POLICY=1)
endif()
if(MAX_PIN_RETRIES)
    add_compile_definitions(MAX_PIN_RETRIES=${MAX_PIN_RETRIES})
endif()
if(FORCE_BUTTON_WAIT)
    add_compile_definitions(FORCE_BUTTON_WAIT=1)
endif()

if(ENABLE_OTP_APP OR ENABLE_OATH_APP)
    set(USB_ITF_CCID 1)
    set(USB_ITF_WCID 1)
else()
    set(USB_ITF_CCID 0)
endif()

set(USB_ITF_HID 1)
include(pico-keys-sdk/picokeys_sdk_import.cmake)

set(SOURCES ${PICOKEYS_SOURCES})

list(APPEND SOURCES
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/fido.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/files.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cmd_register.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cmd_authenticate.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cmd_version.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_reset.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_get_info.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_make_credential.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/known_apps.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_client_pin.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/credential.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_get_assertion.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_selection.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_cred_mgmt.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_config.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_vendor.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/cbor_large_blobs.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/management.c
    ${CMAKE_CURRENT_LIST_DIR}/src/fido/defs.c
)

if(ENABLE_OATH_APP)
    list(APPEND SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/src/fido/oath.c
    )
endif()

if(ENABLE_OTP_APP)
    list(APPEND SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/src/fido/otp.c
    )
endif()

SET_VERSION(ver_major ver_minor "${CMAKE_CURRENT_LIST_DIR}/src/fido/version.h")

set(INCLUDES ${INCLUDES}
    ${CMAKE_CURRENT_LIST_DIR}/src/fido
)

target_sources(rp2354_fido2_key PUBLIC ${SOURCES})
target_include_directories(rp2354_fido2_key PUBLIC ${INCLUDES})

set(COMMON_COMPILE_OPTIONS
    -Wall
)
target_compile_options(rp2354_fido2_key PRIVATE ${COMMON_COMPILE_OPTIONS})

picokeys_apply_strict_flags(
    SOURCES ${SOURCES}
    FILTER_REGEX "/src/fido/|/pico-keys-sdk/src/|/pico-keys-sdk/config/"
)

if(NOT MSVC)
    string(FIND ${CMAKE_C_COMPILER} ":" COMPILER_COLON)
    if(${COMPILER_COLON} GREATER_EQUAL 0)
        target_compile_options(rp2354_fido2_key PRIVATE
            -Wno-error=use-after-free
        )
    endif()
endif()

target_link_libraries(
    rp2354_fido2_key
    PRIVATE
        picokeys_sdk
        pico_stdlib
        pico_multicore
        hardware_flash
        hardware_sync
        hardware_adc
        pico_unique_id
        pico_aon_timer
        tinyusb_device
        tinyusb_board
)
pico_add_extra_outputs(${CMAKE_PROJECT_NAME})
