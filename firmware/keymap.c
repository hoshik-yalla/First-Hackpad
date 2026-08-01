// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌──────────────┬────────────┬──────────────┐
     * │ Ctrl+Shift+P │ Ctrl+Alt+I │ Ctrl+Shift+` │
     * └──────────────┴────────────┴──────────────┘
     */
    [0] = LAYOUT(
        LCTL(LSFT(KC_P)), LCTL(LALT(KC_I)), LCTL(LSFT(KC_GRV))
    )
};

