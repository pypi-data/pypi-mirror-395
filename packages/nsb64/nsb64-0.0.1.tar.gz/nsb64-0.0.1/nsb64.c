#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#if defined(__SSSE3__) || defined(__AVX2__)
#include <immintrin.h>
#endif

#if defined(__ARM_NEON) || defined(__ARM_NEON__)
#include <arm_neon.h>
#endif

static const char base64_table[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static const char base64_url_table[65] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
static const char base32_table[33] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
static const char base32_hex_table[33] = "0123456789ABCDEFGHIJKLMNOPQRSTUV";
static const char base16_table[17] = "0123456789ABCDEF";

static uint8_t base64_dec[256], base64_url_dec[256], base32_dec[256], base32_hex_dec[256];
static uint8_t base16_dec[256];
static int tables_init = 0;

static void init_tables(void) {
    if (tables_init) return;
    
    for (int i = 0; i < 256; i++) {
        base64_dec[i] = 0xFF;
        base64_url_dec[i] = 0xFF;
        base32_dec[i] = 0xFF;
        base32_hex_dec[i] = 0xFF;
        base16_dec[i] = 0xFF;
    }
    
    for (int i = 0; i < 64; i++) {
        base64_dec[(uint8_t)base64_table[i]] = i;
        base64_url_dec[(uint8_t)base64_url_table[i]] = i;
    }
    
    for (int i = 0; i < 32; i++) {
        base32_dec[(uint8_t)base32_table[i]] = i;
        base32_hex_dec[(uint8_t)base32_hex_table[i]] = i;
    }
    
    for (int i = 0; i < 16; i++) {
        base16_dec[(uint8_t)base16_table[i]] = i;
        base16_dec[(uint8_t)tolower(base16_table[i])] = i;
    }
    
    tables_init = 1;
}

#if defined(__AVX2__)
static void b64enc_avx2(const uint8_t* src, size_t len, char* dst) {
    __m256i table = _mm256_loadu_si256((const __m256i*)base64_table);
    __m256i shuffle_mask = _mm256_set_epi8(
        9,8,7, 6,5,4, 10,9,8, 7,6,5, 11,10,9, 8,
        5,4,3, 2,1,0, 6,5,4, 3,2,1, 7,6,5, 4
    );
    
    while (len >= 48) {
        __m256i in1 = _mm256_loadu_si256((const __m256i*)src);
        __m256i in2 = _mm256_loadu_si256((const __m256i*)(src + 24));
        
        __m256i shuf1 = _mm256_shuffle_epi8(in1, shuffle_mask);
        __m256i shuf2 = _mm256_shuffle_epi8(in2, shuffle_mask);
        
        __m256i mask = _mm256_set1_epi8(0x3F);
        __m256i idx1 = _mm256_and_si256(shuf1, mask);
        __m256i idx2 = _mm256_and_si256(shuf2, mask);
        
        __m256i out1 = _mm256_shuffle_epi8(table, idx1);
        __m256i out2 = _mm256_shuffle_epi8(table, idx2);
        
        _mm256_storeu_si256((__m256i*)dst, out1);
        _mm256_storeu_si256((__m256i*)(dst + 32), out2);
        
        src += 48;
        dst += 64;
        len -= 48;
    }
}
#endif

#if defined(__SSSE3__)
static void b64enc_ssse3(const uint8_t* src, size_t len, char* dst) {
    __m128i table = _mm_loadu_si128((const __m128i*)base64_table);
    __m128i shuffle_mask = _mm_set_epi8(
        5,4,3, 2,1,0, 6,5,4, 3,2,1, 7,6,5, 4
    );
    
    while (len >= 24) {
        __m128i in1 = _mm_loadu_si128((const __m128i*)src);
        __m128i in2 = _mm_loadu_si128((const __m128i*)(src + 12));
        
        __m128i shuf1 = _mm_shuffle_epi8(in1, shuffle_mask);
        __m128i shuf2 = _mm_shuffle_epi8(in2, shuffle_mask);
        
        __m128i mask = _mm_set1_epi8(0x3F);
        __m128i idx1 = _mm_and_si128(shuf1, mask);
        __m128i idx2 = _mm_and_si128(shuf2, mask);
        
        __m128i out1 = _mm_shuffle_epi8(table, idx1);
        __m128i out2 = _mm_shuffle_epi8(table, idx2);
        
        _mm_storeu_si128((__m128i*)dst, out1);
        _mm_storeu_si128((__m128i*)(dst + 16), out2);
        
        src += 24;
        dst += 32;
        len -= 24;
    }
}
#endif

#if defined(__ARM_NEON) || defined(__ARM_NEON__)
static void b64enc_neon(const uint8_t* src, size_t len, char* dst) {
    uint8x16_t table = vld1q_u8((const uint8_t*)base64_table);
    
    while (len >= 24) {
        uint8x16x2_t data = vld2q_u8(src);
        uint8x16_t a = data.val[0];
        uint8x16_t b = data.val[1];
        
        uint8x16_t a_shift2 = vshrq_n_u8(a, 2);
        uint8x16_t a_shift4 = vshlq_n_u8(a, 4);
        uint8x16_t b_shift2 = vshrq_n_u8(b, 4);
        uint8x16_t b_shift4 = vshlq_n_u8(b, 2);
        
        uint8x16_t part1 = vorrq_u8(a_shift2, vshrq_n_u8(b_shift4, 6));
        uint8x16_t part2 = vorrq_u8(a_shift4, b_shift2);
        
        uint8x16_t mask = vdupq_n_u8(0x3F);
        uint8x16_t idx1 = vandq_u8(part1, mask);
        uint8x16_t idx2 = vandq_u8(part2, mask);
        
        uint8x16_t out1 = vqtbl1q_u8(table, idx1);
        uint8x16_t out2 = vqtbl1q_u8(table, idx2);
        
        vst1q_u8((uint8_t*)dst, out1);
        vst1q_u8((uint8_t*)(dst + 16), out2);
        
        src += 24;
        dst += 32;
        len -= 24;
    }
}
#endif

static PyObject* b64enc(PyObject* self, PyObject* args, PyObject* kwargs) {
    Py_buffer input;
    PyObject* altchars = NULL;
    static char* kwlist[] = {"input", "altchars", NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|O", kwlist, &input, &altchars))
        return NULL;
    
    const uint8_t* in = input.buf;
    Py_ssize_t in_len = input.len;
    Py_ssize_t out_len = ((in_len + 2) / 3) * 4;
    
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    if (altchars && altchars != Py_None) {
        if (!PyBytes_Check(altchars) || PyBytes_Size(altchars) != 2) {
            PyBuffer_Release(&input); Py_DECREF(result);
            PyErr_SetString(PyExc_ValueError, "altchars must be 2 bytes");
            return NULL;
        }
        char alt1 = PyBytes_AS_STRING(altchars)[0];
        char alt2 = PyBytes_AS_STRING(altchars)[1];
        
        for (; i + 2 < in_len; i += 3, j += 4) {
            uint32_t triple = (in[i] << 16) | (in[i + 1] << 8) | in[i + 2];
            uint8_t c1 = (triple >> 18) & 0x3F;
            uint8_t c2 = (triple >> 12) & 0x3F;
            uint8_t c3 = (triple >> 6) & 0x3F;
            uint8_t c4 = triple & 0x3F;
            
            out[j] = c1 == 62 ? alt1 : base64_table[c1];
            out[j + 1] = c2 == 62 ? alt1 : base64_table[c2];
            out[j + 2] = c3 == 63 ? alt2 : base64_table[c3];
            out[j + 3] = c4 == 63 ? alt2 : base64_table[c4];
        }
    } else {
        #if defined(__AVX2__)
        if (in_len >= 192) {
            b64enc_avx2(in, in_len, out);
            i = (in_len / 48) * 48;
            j = (i / 3) * 4;
        }
        #elif defined(__SSSE3__)
        if (in_len >= 96) {
            b64enc_ssse3(in, in_len, out);
            i = (in_len / 24) * 24;
            j = (i / 3) * 4;
        }
        #elif defined(__ARM_NEON) || defined(__ARM_NEON__)
        if (in_len >= 96) {
            b64enc_neon(in, in_len, out);
            i = (in_len / 24) * 24;
            j = (i / 3) * 4;
        }
        #endif
        
        for (; i + 2 < in_len; i += 3, j += 4) {
            uint32_t triple = (in[i] << 16) | (in[i + 1] << 8) | in[i + 2];
            out[j] = base64_table[(triple >> 18) & 0x3F];
            out[j + 1] = base64_table[(triple >> 12) & 0x3F];
            out[j + 2] = base64_table[(triple >> 6) & 0x3F];
            out[j + 3] = base64_table[triple & 0x3F];
        }
    }
    
    if (i < in_len) {
        uint32_t triple = in[i] << 16;
        if (i + 1 < in_len) triple |= in[i + 1] << 8;
        
        out[j++] = base64_table[(triple >> 18) & 0x3F];
        out[j++] = base64_table[(triple >> 12) & 0x3F];
        
        if (i + 1 < in_len) {
            out[j++] = base64_table[(triple >> 6) & 0x3F];
        } else {
            out[j++] = '=';
        }
        out[j++] = '=';
    }
    
    PyBuffer_Release(&input);
    return result;
}

#if defined(__SSSE3__)
static size_t b64dec_ssse3(const char* src, size_t len, uint8_t* dst) {
    __m128i dec_table = _mm_loadu_si128((const __m128i*)base64_dec);
    __m128i pack_mask = _mm_set_epi8(
        -1,-1,-1,-1, -1,-1,-1,-1, 13,12,11,10, 9,8,7,6
    );
    __m128i shift_mask = _mm_set_epi8(
        5,4,3,2, 1,0,6,5, 4,3,2,1, 0,6,5,4
    );
    
    size_t i = 0, j = 0;
    
    while (i + 16 <= len) {
        __m128i in = _mm_loadu_si128((const __m128i*)(src + i));
        __m128i values = _mm_shuffle_epi8(dec_table, in);
        
        __m128i is_invalid = _mm_cmpeq_epi8(values, _mm_set1_epi8(0xFF));
        if (!_mm_testz_si128(is_invalid, is_invalid)) {
            break;
        }
        
        __m128i packed = _mm_shuffle_epi8(values, pack_mask);
        __m128i shifted = _mm_shuffle_epi8(packed, shift_mask);
        
        __m128i result = _mm_or_si128(
            _mm_slli_epi32(shifted, 6),
            _mm_srli_epi32(shifted, 2)
        );
        
        _mm_storeu_si128((__m128i*)(dst + j), result);
        i += 16;
        j += 12;
    }
    
    return j;
}
#endif

static PyObject* b64dec(PyObject* self, PyObject* args, PyObject* kwargs) {
    Py_buffer input;
    PyObject* altchars = NULL;
    int validate = 0;
    static char* kwlist[] = {"input", "altchars", "validate", NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|Op", kwlist, &input, &altchars, &validate))
        return NULL;
    
    init_tables();
    const char* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    char* temp_buf = NULL;
    uint8_t* dec_table = base64_dec;
    
    if (altchars && altchars != Py_None) {
        if (!PyBytes_Check(altchars) || PyBytes_Size(altchars) != 2) {
            PyBuffer_Release(&input);
            PyErr_SetString(PyExc_ValueError, "altchars must be 2 bytes");
            return NULL;
        }
        
        char alt1 = PyBytes_AS_STRING(altchars)[0];
        char alt2 = PyBytes_AS_STRING(altchars)[1];
        
        temp_buf = malloc(in_len);
        if (!temp_buf) {
            PyBuffer_Release(&input);
            PyErr_NoMemory();
            return NULL;
        }
        
        memcpy(temp_buf, in, in_len);
        in = temp_buf;
        
        for (Py_ssize_t k = 0; k < in_len; k++) {
            if (temp_buf[k] == alt1) temp_buf[k] = '+';
            else if (temp_buf[k] == alt2) temp_buf[k] = '/';
        }
    }
    
    Py_ssize_t padding = 0;
    while (in_len > 0 && in[in_len - 1] == '=') {
        in_len--;
        padding++;
    }
    
    Py_ssize_t out_len = (in_len * 3) / 4;
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { free(temp_buf); PyBuffer_Release(&input); return NULL; }
    
    uint8_t* out = (uint8_t*)PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    #if defined(__SSSE3__)
    if (in_len >= 64 && !temp_buf && !validate) {
        j = b64dec_ssse3(in, in_len, out);
        i = (j / 12) * 16;
    }
    #endif
    
    for (; i + 3 < in_len; i += 4, j += 3) {
        uint32_t quad = 0;
        for (int k = 0; k < 4; k++) {
            uint8_t val = dec_table[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base64 character");
                return NULL;
            }
            quad = (quad << 6) | val;
        }
        out[j] = (quad >> 16) & 0xFF;
        out[j + 1] = (quad >> 8) & 0xFF;
        out[j + 2] = quad & 0xFF;
    }
    
    if (padding && i < in_len) {
        uint32_t quad = 0;
        int remaining = in_len - i;
        
        for (int k = 0; k < remaining; k++) {
            uint8_t val = dec_table[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base64 character");
                return NULL;
            }
            quad = (quad << 6) | val;
        }
        
        quad <<= (4 - remaining) * 6;
        out[j++] = (quad >> 16) & 0xFF;
        if (remaining > 2) out[j++] = (quad >> 8) & 0xFF;
    }
    
    if (j < out_len) {
        if (_PyBytes_Resize(&result, j) < 0) {
            free(temp_buf); PyBuffer_Release(&input);
            return NULL;
        }
    }
    
    free(temp_buf);
    PyBuffer_Release(&input);
    return result;
}

static PyObject* b32encode(PyObject* self, PyObject* args) {
    Py_buffer input;
    
    if (!PyArg_ParseTuple(args, "y*", &input))
        return NULL;
    
    const uint8_t* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    Py_ssize_t out_len = ((in_len + 4) / 5) * 8;
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    for (; i + 4 < in_len; i += 5, j += 8) {
        uint64_t quint = ((uint64_t)in[i] << 32) |
                        ((uint64_t)in[i + 1] << 24) |
                        ((uint64_t)in[i + 2] << 16) |
                        ((uint64_t)in[i + 3] << 8) |
                        in[i + 4];
        
        out[j] = base32_table[(quint >> 35) & 0x1F];
        out[j + 1] = base32_table[(quint >> 30) & 0x1F];
        out[j + 2] = base32_table[(quint >> 25) & 0x1F];
        out[j + 3] = base32_table[(quint >> 20) & 0x1F];
        out[j + 4] = base32_table[(quint >> 15) & 0x1F];
        out[j + 5] = base32_table[(quint >> 10) & 0x1F];
        out[j + 6] = base32_table[(quint >> 5) & 0x1F];
        out[j + 7] = base32_table[quint & 0x1F];
    }
    
    if (i < in_len) {
        uint64_t quint = 0;
        int remaining = in_len - i;
        
        for (int k = 0; k < remaining; k++) {
            quint |= (uint64_t)in[i + k] << (8 * (4 - k));
        }
        
        int chars_to_output;
        switch (remaining) {
            case 1: chars_to_output = 2; break; 
            case 2: chars_to_output = 4; break; 
            case 3: chars_to_output = 5; break; 
            case 4: chars_to_output = 7; break; 
            default: chars_to_output = 0;
        }
        
        if (chars_to_output >= 1) out[j++] = base32_table[(quint >> 35) & 0x1F];
        if (chars_to_output >= 2) out[j++] = base32_table[(quint >> 30) & 0x1F];
        if (chars_to_output >= 3) out[j++] = base32_table[(quint >> 25) & 0x1F];
        if (chars_to_output >= 4) out[j++] = base32_table[(quint >> 20) & 0x1F];
        if (chars_to_output >= 5) out[j++] = base32_table[(quint >> 15) & 0x1F];
        if (chars_to_output >= 6) out[j++] = base32_table[(quint >> 10) & 0x1F];
        if (chars_to_output >= 7) out[j++] = base32_table[(quint >> 5) & 0x1F];
        
        // Добавляем padding до 8 символов
        while (j < out_len) {
            out[j++] = '=';
        }
    }
    
    PyBuffer_Release(&input);
    return result;
}

static PyObject* b32decode(PyObject* self, PyObject* args, PyObject* kwargs) {
    Py_buffer input;
    int casefold = 0;
    PyObject* map01 = NULL;
    static char* kwlist[] = {"input", "casefold", "map01", NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|pO", kwlist, &input, &casefold, &map01))
        return NULL;
    
    init_tables();
    char* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    if (in_len == 0) {
        PyBuffer_Release(&input);
        return PyBytes_FromStringAndSize("", 0);
    }
    
    if (in_len % 8) {
        PyBuffer_Release(&input);
        PyErr_SetString(PyExc_ValueError, "Input length must be multiple of 8");
        return NULL;
    }
    
    char* temp_buf = malloc(in_len);
    if (!temp_buf) {
        PyBuffer_Release(&input);
        PyErr_NoMemory();
        return NULL;
    }
    
    memcpy(temp_buf, in, in_len);
    in = temp_buf;
    
    if (map01 && map01 != Py_None) {
        if (!PyBytes_Check(map01) || PyBytes_Size(map01) != 1) {
            free(temp_buf); PyBuffer_Release(&input);
            PyErr_SetString(PyExc_ValueError, "map01 must be 1 byte");
            return NULL;
        }
        char m = PyBytes_AS_STRING(map01)[0];
        for (Py_ssize_t i = 0; i < in_len; i++) {
            if (in[i] == '0') in[i] = 'O';
            else if (in[i] == '1') in[i] = m;
        }
    }
    
    if (casefold) {
        for (Py_ssize_t i = 0; i < in_len; i++) {
            in[i] = toupper((unsigned char)in[i]);
        }
    }
    
    Py_ssize_t padding = 0;
    while (in_len > 0 && in[in_len - 1] == '=') {
        in_len--;
        padding++;
    }
    
    static const int valid_padding[8] = {1, 0, 0, 1, 0, 0, 1, 0};
    if (padding > 0 && !valid_padding[padding]) {
        free(temp_buf); PyBuffer_Release(&input);
        PyErr_SetString(PyExc_ValueError, "Invalid padding");
        return NULL;
    }
    
    Py_ssize_t out_len = (in_len * 5) / 8;
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { free(temp_buf); PyBuffer_Release(&input); return NULL; }
    
    uint8_t* out = (uint8_t*)PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    for (; i + 7 < in_len; i += 8, j += 5) {
        uint64_t oct = 0;
        for (int k = 0; k < 8; k++) {
            uint8_t val = base32_dec[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base32 character");
                return NULL;
            }
            oct = (oct << 5) | val;
        }
        out[j] = (oct >> 32) & 0xFF;
        out[j + 1] = (oct >> 24) & 0xFF;
        out[j + 2] = (oct >> 16) & 0xFF;
        out[j + 3] = (oct >> 8) & 0xFF;
        out[j + 4] = oct & 0xFF;
    }
    
    if (padding > 0 && i < in_len) {
        uint64_t oct = 0;
        int remaining = in_len - i;
        
        for (int k = 0; k < remaining; k++) {
            uint8_t val = base32_dec[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base32 character");
                return NULL;
            }
            oct = (oct << 5) | val;
        }
        
        oct <<= (8 - remaining) * 5;
        out[j++] = (oct >> 32) & 0xFF;
        if (remaining > 2) out[j++] = (oct >> 24) & 0xFF;
        if (remaining > 4) out[j++] = (oct >> 16) & 0xFF;
        if (remaining > 5) out[j++] = (oct >> 8) & 0xFF;
        if (remaining > 7) out[j++] = oct & 0xFF;
    }
    
    if (j < out_len) {
        if (_PyBytes_Resize(&result, j) < 0) {
            free(temp_buf); PyBuffer_Release(&input);
            return NULL;
        }
    }
    
    free(temp_buf);
    PyBuffer_Release(&input);
    return result;
}

static PyObject* b32hexencode(PyObject* self, PyObject* args) {
    Py_buffer input;
    
    if (!PyArg_ParseTuple(args, "y*", &input))
        return NULL;
    
    const uint8_t* in = input.buf;
    Py_ssize_t in_len = input.len;
    Py_ssize_t out_len = ((in_len + 4) / 5) * 8;
    
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    for (; i + 4 < in_len; i += 5, j += 8) {
        uint64_t quint = ((uint64_t)in[i] << 32) |
                        ((uint64_t)in[i + 1] << 24) |
                        ((uint64_t)in[i + 2] << 16) |
                        ((uint64_t)in[i + 3] << 8) |
                        in[i + 4];
        
        out[j] = base32_hex_table[(quint >> 35) & 0x1F];
        out[j + 1] = base32_hex_table[(quint >> 30) & 0x1F];
        out[j + 2] = base32_hex_table[(quint >> 25) & 0x1F];
        out[j + 3] = base32_hex_table[(quint >> 20) & 0x1F];
        out[j + 4] = base32_hex_table[(quint >> 15) & 0x1F];
        out[j + 5] = base32_hex_table[(quint >> 10) & 0x1F];
        out[j + 6] = base32_hex_table[(quint >> 5) & 0x1F];
        out[j + 7] = base32_hex_table[quint & 0x1F];
    }
    
    if (i < in_len) {
        uint64_t quint = 0;
        int remaining = in_len - i;
        
        for (int k = 0; k < remaining; k++) {
            quint |= (uint64_t)in[i + k] << (8 * (4 - k));
        }
        
        static const int padding_count[5] = {0, 6, 4, 3, 1};
        int pad_chars = 8 - ((remaining * 8 + 4) / 5);
        
        out[j++] = base32_hex_table[(quint >> 35) & 0x1F];
        out[j++] = base32_hex_table[(quint >> 30) & 0x1F];
        
        if (remaining > 1) out[j++] = base32_hex_table[(quint >> 25) & 0x1F];
        if (remaining > 2) out[j++] = base32_hex_table[(quint >> 20) & 0x1F];
        if (remaining > 3) out[j++] = base32_hex_table[(quint >> 15) & 0x1F];
        if (remaining > 4) out[j++] = base32_hex_table[(quint >> 10) & 0x1F];
        if (remaining > 5) out[j++] = base32_hex_table[(quint >> 5) & 0x1F];
        if (remaining > 6) out[j++] = base32_hex_table[quint & 0x1F];
        
        for (int p = 0; p < pad_chars; p++) {
            out[j++] = '=';
        }
    }
    
    PyBuffer_Release(&input);
    return result;
}

static PyObject* base16_encode(PyObject* self, PyObject* args) {
    Py_buffer input;
    
    if (!PyArg_ParseTuple(args, "y*", &input))
        return NULL;
    
    const uint8_t* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    PyObject* result = PyBytes_FromStringAndSize(NULL, in_len * 2);
    if (!result) { PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    
    #if defined(__SSE2__) || defined(__AVX2__)
    if (in_len >= 32) {
        #if defined(__AVX2__)
        __m256i nibble_mask = _mm256_set1_epi8(0x0F);
        __m256i hex_table = _mm256_loadu_si256((const __m256i*)base16_table);
        
        while (in_len >= 32) {
            __m256i data = _mm256_loadu_si256((const __m256i*)in);
            __m256i hi_nibbles = _mm256_and_si256(_mm256_srli_epi16(data, 4), nibble_mask);
            __m256i lo_nibbles = _mm256_and_si256(data, nibble_mask);
            
            __m256i hi_chars = _mm256_shuffle_epi8(hex_table, hi_nibbles);
            __m256i lo_chars = _mm256_shuffle_epi8(hex_table, lo_nibbles);
            
            __m256i interleaved = _mm256_unpacklo_epi8(hi_chars, lo_chars);
            __m256i packed = _mm256_permute4x64_epi64(interleaved, 0xD8);
            
            _mm256_storeu_si256((__m256i*)out, packed);
            
            in += 32;
            out += 64;
            in_len -= 32;
        }
        #elif defined(__SSE2__)
        __m128i nibble_mask = _mm_set1_epi8(0x0F);
        __m128i hex_table = _mm_loadu_si128((const __m128i*)base16_table);
        
        while (in_len >= 16) {
            __m128i data = _mm_loadu_si128((const __m128i*)in);
            __m128i hi_nibbles = _mm_and_si128(_mm_srli_epi16(data, 4), nibble_mask);
            __m128i lo_nibbles = _mm_and_si128(data, nibble_mask);
            
            __m128i hi_chars = _mm_shuffle_epi8(hex_table, hi_nibbles);
            __m128i lo_chars = _mm_shuffle_epi8(hex_table, lo_nibbles);
            
            __m128i interleaved_lo = _mm_unpacklo_epi8(hi_chars, lo_chars);
            __m128i interleaved_hi = _mm_unpackhi_epi8(hi_chars, lo_chars);
            
            _mm_storeu_si128((__m128i*)out, interleaved_lo);
            _mm_storeu_si128((__m128i*)(out + 16), interleaved_hi);
            
            in += 16;
            out += 32;
            in_len -= 16;
        }
        #endif
    }
    #endif
    
    for (Py_ssize_t i = 0; i < in_len; i++) {
        uint8_t byte = in[i];
        out[i * 2] = base16_table[byte >> 4];
        out[i * 2 + 1] = base16_table[byte & 0x0F];
    }
    
    PyBuffer_Release(&input);
    return result;
}

static PyObject* base16_decode(PyObject* self, PyObject* args, PyObject* kwargs) {
    Py_buffer input;
    int casefold = 0;
    static char* kwlist[] = {"input", "casefold", NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*|p", kwlist, &input, &casefold))
        return NULL;
    
    init_tables();
    char* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    if (in_len % 2 != 0) {
        PyBuffer_Release(&input);
        PyErr_SetString(PyExc_ValueError, "Invalid base16 length");
        return NULL;
    }
    
    char* temp_buf = malloc(in_len);
    if (!temp_buf) {
        PyBuffer_Release(&input);
        PyErr_NoMemory();
        return NULL;
    }
    
    memcpy(temp_buf, in, in_len);
    in = temp_buf;
    
    if (casefold) {
        for (Py_ssize_t i = 0; i < in_len; i++) {
            if (in[i] >= 'a' && in[i] <= 'f') {
                in[i] -= 32;
            }
        }
    }
    
    Py_ssize_t out_len = in_len / 2;
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { free(temp_buf); PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    
    #if defined(__SSSE3__) || defined(__AVX2__)
    if (in_len >= 64) {
        #if defined(__AVX2__)
        __m256i ascii0 = _mm256_set1_epi8('0');
        __m256i ascii9 = _mm256_set1_epi8('9' + 1);
        __m256i asciiA = _mm256_set1_epi8('A');
        __m256i asciiF = _mm256_set1_epi8('F' + 1);
        __m256i adjust_num = _mm256_set1_epi8(0);
        __m256i adjust_alpha = _mm256_set1_epi8(9);
        
        while (in_len >= 64) {
            __m256i data1 = _mm256_loadu_si256((const __m256i*)in);
            __m256i data2 = _mm256_loadu_si256((const __m256i*)(in + 32));
            
            __m256i is_digit1 = _mm256_and_si256(
                _mm256_cmpgt_epi8(data1, ascii0),
                _mm256_cmpgt_epi8(ascii9, data1)
            );
            __m256i is_alpha1 = _mm256_and_si256(
                _mm256_cmpgt_epi8(data1, asciiA),
                _mm256_cmpgt_epi8(asciiF, data1)
            );
            
            __m256i is_digit2 = _mm256_and_si256(
                _mm256_cmpgt_epi8(data2, ascii0),
                _mm256_cmpgt_epi8(ascii9, data2)
            );
            __m256i is_alpha2 = _mm256_and_si256(
                _mm256_cmpgt_epi8(data2, asciiA),
                _mm256_cmpgt_epi8(asciiF, data2)
            );
            
            __m256i valid1 = _mm256_or_si256(is_digit1, is_alpha1);
            __m256i valid2 = _mm256_or_si256(is_digit2, is_alpha2);
            
            if (!_mm256_testc_si256(valid1, _mm256_set1_epi8(-1)) ||
                !_mm256_testc_si256(valid2, _mm256_set1_epi8(-1))) {
                break;
            }
            
            __m256i digit_val1 = _mm256_sub_epi8(data1, ascii0);
            __m256i alpha_val1 = _mm256_sub_epi8(data1, _mm256_sub_epi8(asciiA, adjust_alpha));
            __m256i val1 = _mm256_blendv_epi8(digit_val1, alpha_val1, is_alpha1);
            
            __m256i digit_val2 = _mm256_sub_epi8(data2, ascii0);
            __m256i alpha_val2 = _mm256_sub_epi8(data2, _mm256_sub_epi8(asciiA, adjust_alpha));
            __m256i val2 = _mm256_blendv_epi8(digit_val2, alpha_val2, is_alpha2);
            
            __m256i hi_nibbles = _mm256_slli_epi16(val1, 4);
            __m256i lo_nibbles = val2;
            __m256i combined = _mm256_or_si256(hi_nibbles, lo_nibbles);
            
            _mm256_storeu_si256((__m256i*)out, combined);
            
            in += 64;
            out += 32;
            in_len -= 64;
        }
        #endif
    }
    #endif
    
    for (Py_ssize_t i = 0; i < in_len; i += 2) {
        uint8_t high = base16_dec[(uint8_t)in[i]];
        uint8_t low = base16_dec[(uint8_t)in[i + 1]];
        
        if (high == 0xFF || low == 0xFF) {
            free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
            PyErr_SetString(PyExc_ValueError, "Invalid base16 digit");
            return NULL;
        }
        
        out[i / 2] = (high << 4) | low;
    }
    
    free(temp_buf);
    PyBuffer_Release(&input);
    return result;
}

static PyObject* urlsafe_b64enc(PyObject* self, PyObject* args) {
    Py_buffer input;
    
    if (!PyArg_ParseTuple(args, "y*", &input))
        return NULL;
    
    const uint8_t* in = input.buf;
    Py_ssize_t in_len = input.len;
    Py_ssize_t out_len = ((in_len + 2) / 3) * 4;
    
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { PyBuffer_Release(&input); return NULL; }
    
    char* out = PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    for (; i + 2 < in_len; i += 3, j += 4) {
        uint32_t triple = (in[i] << 16) | (in[i + 1] << 8) | in[i + 2];
        out[j] = base64_url_table[(triple >> 18) & 0x3F];
        out[j + 1] = base64_url_table[(triple >> 12) & 0x3F];
        out[j + 2] = base64_url_table[(triple >> 6) & 0x3F];
        out[j + 3] = base64_url_table[triple & 0x3F];
    }
    
    if (i < in_len) {
        uint32_t triple = in[i] << 16;
        if (i + 1 < in_len) triple |= in[i + 1] << 8;
        
        out[j++] = base64_url_table[(triple >> 18) & 0x3F];
        out[j++] = base64_url_table[(triple >> 12) & 0x3F];
        
        if (i + 1 < in_len) {
            out[j++] = base64_url_table[(triple >> 6) & 0x3F];
        } else {
            out[j++] = '=';
        }
        out[j++] = '=';
    }
    
    PyBuffer_Release(&input);
    return result;
}

static PyObject* urlsafe_b64dec(PyObject* self, PyObject* args) {
    Py_buffer input;
    
    if (!PyArg_ParseTuple(args, "y*", &input))
        return NULL;
    
    init_tables();
    const char* in = input.buf;
    Py_ssize_t in_len = input.len;
    
    char* temp_buf = malloc(in_len);
    if (!temp_buf) {
        PyBuffer_Release(&input);
        PyErr_NoMemory();
        return NULL;
    }
    
    memcpy(temp_buf, in, in_len);
    in = temp_buf;
    
    for (Py_ssize_t i = 0; i < in_len; i++) {
        if (temp_buf[i] == '-') temp_buf[i] = '+';
        else if (temp_buf[i] == '_') temp_buf[i] = '/';
    }
    
    Py_ssize_t padding = 0;
    while (in_len > 0 && in[in_len - 1] == '=') {
        in_len--;
        padding++;
    }
    
    Py_ssize_t out_len = (in_len * 3) / 4;
    PyObject* result = PyBytes_FromStringAndSize(NULL, out_len);
    if (!result) { free(temp_buf); PyBuffer_Release(&input); return NULL; }
    
    uint8_t* out = (uint8_t*)PyBytes_AS_STRING(result);
    Py_ssize_t i = 0, j = 0;
    
    for (; i + 3 < in_len; i += 4, j += 3) {
        uint32_t quad = 0;
        for (int k = 0; k < 4; k++) {
            uint8_t val = base64_dec[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base64 character");
                return NULL;
            }
            quad = (quad << 6) | val;
        }
        out[j] = (quad >> 16) & 0xFF;
        out[j + 1] = (quad >> 8) & 0xFF;
        out[j + 2] = quad & 0xFF;
    }
    
    if (padding && i < in_len) {
        uint32_t quad = 0;
        int remaining = in_len - i;
        
        for (int k = 0; k < remaining; k++) {
            uint8_t val = base64_dec[(uint8_t)in[i + k]];
            if (val == 0xFF) {
                free(temp_buf); PyBuffer_Release(&input); Py_DECREF(result);
                PyErr_SetString(PyExc_ValueError, "Invalid base64 character");
                return NULL;
            }
            quad = (quad << 6) | val;
        }
        
        quad <<= (4 - remaining) * 6;
        out[j++] = (quad >> 16) & 0xFF;
        if (remaining > 2) out[j++] = (quad >> 8) & 0xFF;
    }
    
    if (j < out_len) {
        if (_PyBytes_Resize(&result, j) < 0) {
            free(temp_buf); PyBuffer_Release(&input);
            return NULL;
        }
    }
    
    free(temp_buf);
    PyBuffer_Release(&input);
    return result;
}

static PyMethodDef module_methods[] = {
    {"b64enc", (PyCFunction)b64enc, METH_VARARGS | METH_KEYWORDS, "Base64 encode"},
    {"b64dec", (PyCFunction)b64dec, METH_VARARGS | METH_KEYWORDS, "Base64 decode"},
    {"b32encode", b32encode, METH_VARARGS, "Base32 encode"},
    {"b32decode", (PyCFunction)b32decode, METH_VARARGS | METH_KEYWORDS, "Base32 decode"},
    {"b32hexencode", b32hexencode, METH_VARARGS, "Base32 hex encode"},
    {"b16encode", base16_encode, METH_VARARGS, "Base16 encode"},
    {"b16decode", (PyCFunction)base16_decode, METH_VARARGS | METH_KEYWORDS, "Base16 decode"},
    {"urlsafe_b64enc", urlsafe_b64enc, METH_VARARGS, "URL-safe Base64 encode"},
    {"urlsafe_b64dec", urlsafe_b64dec, METH_VARARGS, "URL-safe Base64 decode"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "nsb64",
    NULL,
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_nsb64(void) {
    init_tables();
    return PyModule_Create(&module_def);
}