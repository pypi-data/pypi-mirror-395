/**
 * pmsys_minimal.hpp
 *
 * Minimal PMSYS header for Python coordinate_system bindings
 * Contains only: vec3, vec2, quat, coord3 and their dependencies
 *
 * Author: PanGuoJun
 * Version: 1.2.0
 */

#pragma once
#ifndef PMSYS_MINIMAL_HPP
#define PMSYS_MINIMAL_HPP

// ==============================================================================
// Standard headers
// ==============================================================================
#ifdef _WIN32
#define WINDOWS
#endif

#include <map>
#include <array>
#include <functional>
#include <string>
#include <vector>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdarg.h>
#include <math.h>
#include <tgmath.h>
#include <algorithm>
#include <list>
#include <sstream>
#include <fstream>
#include <iostream>
#include <set>
#include <queue>
#include <regex>
#include <numeric>
#include <stdexcept>
#include <any>
#include <filesystem>
#include <unordered_set>
#include <random>
#include <limits>
#include <mutex>
#include <memory>

#if defined(_MSC_VER)
#include <execution>
#endif

// Disable warnings
#pragma warning(disable:4244)
#pragma warning(disable:4305)
#pragma warning(disable:4267)
#pragma warning(disable:4819)
#pragma warning(disable:4018)
#pragma warning(disable:4005)

// ==============================================================================
// Type definitions
// ==============================================================================
#define real                double
#define EPSILON             1e-5
#define DEVICE_CALLABLE
#define EXPORT_API

// Aliases
#define anyptr              void*
#define crstr               const std::string&
#define uchar               unsigned char
#define u8                  unsigned char
#define u16                 unsigned short
#define u32                 unsigned int
#define uint                unsigned int

#define vec3                vector3
#define rvec                vector3&
#define crvec               const vector3&

#define vec2                vector2
#define rvec2               vector2&
#define crvec2              const vector2&

#define vec4                vector4
#define rvec4               vector4&
#define crvec4              const vector4&

#define quat                quaternion
#define crquat              const quaternion&

#define crd3                coord3
#define rcd3                coord3&
#define crcd3               const coord3&

// Constants
#define PI                  3.14159265358979323846264338327950288
#define TWOPI               (2 * PI)
#define INFINITY            std::numeric_limits<real>::infinity()
#define REAL_MAX            INFINITY

using namespace std;

// ==============================================================================
// Tolerance definitions
// ==============================================================================
const real c_tor_dis_level_2    = 1e-1;
const real c_tor_dis_level_1    = 1e-2;
const real c_tor_dis_level0     = 1e-3;
const real c_tor_dis_level1     = 1e-4;
const real c_tor_dis_level2     = 1e-5;
const real c_tor_dis_level3     = 1e-6;
const real c_tor_dis_level3_    = 1e-7;
const real c_tor_dis_level4     = 1e-8;
const real c_tor_dis_level5     = 1e-10;

// ==============================================================================
// Utility functions
// ==============================================================================
inline real rrnd(real min = 0.0, real max = 1.0) {
    return (max) == (min) ? (min) : (min)+((real)(rand()) / (RAND_MAX + 1.0)) * ((max)-(min));
}

inline int rndi(int min, int max) {
    return min == max ? min : rand() % (max - min + 1) + min;
}

inline bool is_zero(real x, real tor = 1e-5) {
    return fabs(x) < tor;
}

inline bool check_equal(real a, real b, const real eps = EPSILON) {
    return (::fabs(a - b) <= eps);
}

inline real fract(real x) {
    return x - floor(x);
}

inline real radians(real deg) {
    return deg / 180.0 * PI;
}

inline real lerp(real h1, real h2, real alpha) {
    return h1 * (1.0 - alpha) + h2 * alpha;
}

// ==============================================================================
// Coordinate System Handedness (Left/Right)
// ==============================================================================
namespace {
    // Global handedness setting: true = left-handed (default), false = right-handed
    bool g_use_left_handed_system = true;
}

// Set coordinate system handedness
inline void set_coordinate_handedness(bool use_left_handed) {
    g_use_left_handed_system = use_left_handed;
}

// Get current coordinate system handedness
inline bool get_coordinate_handedness() {
    return g_use_left_handed_system;
}


inline real sign(real x) {
    return x < 0 ? -1.0 : (x > 0 ? 1.0 : 0.0);
}

// 三次插值函数 (需要在 quaternion 类之前定义)
inline real cubic_interpolate(real p_from, real p_to, real p_pre, real p_post, real p_weight) {
    return 0.5 * ((p_from * 2.0) +
        (-p_pre + p_to) * p_weight +
        (2.0 * p_pre - 5.0 * p_from + 4.0 * p_to - p_post) * (p_weight * p_weight) +
        (-p_pre + 3.0 * p_from - 3.0 * p_to + p_post) * (p_weight * p_weight * p_weight));
}

// 调试宏 (需要在 coord.hpp 之前定义)
#define GCU_VERSION "1.02"
#define PRINT(msg)              {}
#define PRINTVEC3(v)            {}
#define PRINTVEC2(v)            {}

inline real clamp(real x, real minval, real maxval) {
    return x < minval ? minval : (x > maxval ? maxval : x);
}

inline real _MIN(real a, real b) {
    return ((a) < (b) ? (a) : (b));
}

inline real _MAX(real a, real b) {
    return ((a) > (b) ? (a) : (b));
}

inline real _MINV(real a, real b, real c) {
    return _MIN(_MIN(a, b), c);
}

inline real _MAXV(real a, real b, real c) {
    return _MAX(_MAX(a, b), c);
}

// Hash function
template <typename T>
inline void hash_combine(std::size_t& seed, const T& v) {
    seed ^= v + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

inline void hash_combine(std::size_t& seed, const real& v) {
    seed ^= std::hash<real>{}(v)+0x9e3779b9 + (seed << 6) + (seed >> 2);
}

// ==============================================================================
// PMSYS 核心类定义开始
// ==============================================================================

/**
 *						【向量】
 *
 *					向量的定义是来自于四元数
 *					向量不是完整的数，
 *					向量跟空间结构有关系，
 *					如果在时空中建议使用四元数
 */
// **********************************************************************
// 2D
// **********************************************************************
#pragma once
struct vector2
{
    static const vector2 ZERO;
    static const vector2 ONE;
    static const vector2 UX;
    static const vector2 UY;
    static const vector2 CENTER;
    static const vector2 INFINITY2;
    static real sEPSILON;

    union {
        real val[2];
        struct
        {
            real x;
            real y;
        };
    };

    real& operator[](int ind)
    {
        return val[ind];
    }
    DEVICE_CALLABLE vector2()
    {
        x = 0;
        y = 0;
    }
    DEVICE_CALLABLE vector2(const vector2& v)
    {
        x = v.x;
        y = v.y;
    }
    DEVICE_CALLABLE explicit vector2(real v)
    {
        x = v;
        y = v;
    }
    DEVICE_CALLABLE vector2(real _x, real _y)
    {
        x = _x;
        y = _y;
    }

    DEVICE_CALLABLE static vector2 ang_len(real _angle, real _r)
    {
        return vector2(_r * cos(_angle), _r * sin(_angle));
    }

    bool isINF() const
    {
        return x == INFINITY || y == INFINITY || x == -INFINITY || y == -INFINITY;
    }

    DEVICE_CALLABLE vector2 xx() const { return vector2(x, x); }
    DEVICE_CALLABLE vector2 xy() const { return vector2(x, y); }
    DEVICE_CALLABLE vector2 yx() const { return vector2(y, x); }
    DEVICE_CALLABLE vector2 yy() const { return vector2(y, y); }

    DEVICE_CALLABLE vector2 operator+(const vector2& _p) const
    {
        vector2 fp;
        fp.x = x + _p.x;
        fp.y = y + _p.y;

        return fp;
    }
    DEVICE_CALLABLE void operator+=(const vector2& _p)
    {
        x += _p.x;
        y += _p.y;
    }
    DEVICE_CALLABLE vector2 operator-(const vector2& _p) const
    {
        vector2 fp;
        fp.x = x - _p.x;
        fp.y = y - _p.y;
        return fp;
    }
    DEVICE_CALLABLE void operator-=(const vector2& _p)
    {
        x = x - _p.x;
        y = y - _p.y;
    }
    DEVICE_CALLABLE vector2 operator-() const
    {
        vector2 fp;
        fp.x = -x;
        fp.y = -y;
        return fp;
    }

    DEVICE_CALLABLE bool operator<(const vector2& rv) const
    {
        if (x < rv.x && y < rv.y)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator<=(const vector2& rv) const
    {
        if (x <= rv.x && y <= rv.y)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator>(const vector2& rv) const
    {
        if (x > rv.x && y > rv.y)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator>=(const vector2& rv) const
    {
        if (x >= rv.x && y >= rv.y)
            return true;
        return false;
    }
    DEVICE_CALLABLE vector2 operator*(real s) const
    {
        vector2 fp;
        fp.x = s * x;
        fp.y = s * y;
        return fp;
    }
    DEVICE_CALLABLE void operator*=(real s)
    {
        x = s * x;
        y = s * y;
    }
    DEVICE_CALLABLE friend vector2 operator*(real s, const vector2& v)
    {
        vector2 fp;
        fp.x = v.x * s;
        fp.y = v.y * s;
        return fp;
    }
    DEVICE_CALLABLE vector2 operator*(const vector2& b) const
    {
        return vector2(x * b.x, y * b.y);
    }
    DEVICE_CALLABLE void operator*=(const vector2& b)
    {
        x = x * b.x;
        y = y * b.y;
    }
    DEVICE_CALLABLE vector2 operator/(real s) const
    {
        vector2 fp;
        fp.x = x / s;
        fp.y = y / s;
        return fp;
    }
    DEVICE_CALLABLE vector2 operator/(const vector2& b) const
    {
        vector2 fp;
        fp.x = x / b.x;
        fp.y = y / b.y;
        return fp;
    }
    DEVICE_CALLABLE void operator/=(const vector2& b)
    {
        x = x / b.x;
        y = y / b.y;
    }
    DEVICE_CALLABLE void operator/=(real s)
    {
        x = x / s;
        y = y / s;
    }
    DEVICE_CALLABLE bool operator==(const vector2& rv) const
    {
        return (fabs(x - rv.x) <= sEPSILON && fabs(y - rv.y) <= sEPSILON);
    }
    DEVICE_CALLABLE bool operator!=(const vector2& rv) const
    {
        return (fabs(x - rv.x) > sEPSILON || fabs(y - rv.y) > sEPSILON);
    }
    DEVICE_CALLABLE real len() const
    {
        return sqrt(x * x + y * y);
    }
    DEVICE_CALLABLE real length() const
    {
        return sqrt(x * x + y * y);
    }
    DEVICE_CALLABLE real sqrlen() const
    {
        return (x * x + y * y);
    }
    DEVICE_CALLABLE real angle() const
    {
        return atan2(y, x);
    }
    DEVICE_CALLABLE vector2 angle(real ang)
    {
        return ang_len(ang, 1);
    }
    DEVICE_CALLABLE void normalize()
    {
        real r = len();
        if (r > sEPSILON)
        {
            x /= r;
            y /= r;
        }
    }
    DEVICE_CALLABLE vector2 normcopy() const
    {
        real r = len();
        if (r > sEPSILON)
        {
            return vector2(x / r, y / r);
        }
        return vector2(0, 0);
    }
    DEVICE_CALLABLE vector2 normalized() const
    {
        real r = len();
        if (r > sEPSILON)
        {
            return vector2(x / r, y / r);
        }
        return vector2(0, 0);
    }
    DEVICE_CALLABLE void rot(real angle)
    {
        (*this) = complex_mul((*this), vector2::ang_len(angle, 1));
    }
    DEVICE_CALLABLE vector2 rotcopy(real angle) const
    {
        return complex_mul((*this), vector2::ang_len(angle, 1));
    }
    DEVICE_CALLABLE vector2 rotcpy(real angle) const
    {
        return complex_mul((*this), vector2::ang_len(angle, 1));
    }
    DEVICE_CALLABLE vector2 roted(real angle) const
    {
        return complex_mul((*this), vector2::ang_len(angle, 1));
    }
    DEVICE_CALLABLE void rot(real angle, const vector2& o)
    {
        vector2 v = (*this) - o;
        v = complex_mul(v, vector2::ang_len(angle, 1));
        (*this) = v + o;
    }
    DEVICE_CALLABLE vector2 rotcopy(real angle, const vector2& o) const
    {
        vector2 v = (*this) - o;
        v = complex_mul(v, vector2::ang_len(angle, 1));
        return v + o;
    }
    DEVICE_CALLABLE vector2 rotcpy(real angle, const vector2& o) const
    {
        vector2 v = (*this) - o;
        v = complex_mul(v, vector2::ang_len(angle, 1));
        return v + o;
    }
    DEVICE_CALLABLE vector2 roted(real angle, const vector2& o) const
    {
        vector2 v = (*this) - o;
        v = complex_mul(v, vector2::ang_len(angle, 1));
        return v + o;
    }
    DEVICE_CALLABLE friend vector2 complex_mul(const vector2& a, const vector2& b)
    {
        return vector2(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x);
    }
    DEVICE_CALLABLE real dot(const vector2& v) const
    {
        return x * v.x + y * v.y;
    }
    DEVICE_CALLABLE real cross(const vector2& v) const
    {
        return x * v.y - y * v.x;
    }
    std::string serialise() const
    {
        return std::to_string(x) + "," + std::to_string(y);
    }
};

inline const vector2 vector2::ZERO = vector2(0, 0);
inline const vector2 vector2::ONE = vector2(1, 1);
inline const vector2 vector2::UX = vector2(1, 0);
inline const vector2 vector2::UY = vector2(0, 1);
inline const vector2 vector2::CENTER = vector2(0.5f, 0.5f);
inline const vector2 vector2::INFINITY2 = vector2(INFINITY, INFINITY);
inline real vector2::sEPSILON = EPSILON;

// **********************************************************************
// 3D
// **********************************************************************
struct vector3
{
    static const vector3 ZERO;
    static const vector3 ONE;
    static const vector3 UX;
    static const vector3 UY;
    static const vector3 UZ;
    static const vector3 CENTER;
    static const vector3 INFINITY3;
    static real sEPSILON;

    union {
        real val[3];
        struct
        {
            real x;
            real y;
            real z;
        };
    };
    DEVICE_CALLABLE vector3()
    {
        x = 0;
        y = 0;
        z = 0;
    }
    DEVICE_CALLABLE explicit vector3(int v)
    {
        x = (real)v;
        y = (real)v;
        z = (real)v;
    }
    DEVICE_CALLABLE explicit vector3(real v)
    {
        x = v;
        y = v;
        z = v;
    }
    DEVICE_CALLABLE explicit vector3(real* v)
    {
        x = v[0];
        y = v[1];
        z = v[2];
    }
    DEVICE_CALLABLE vector3(real _x, real _y, real _z = 0)
    {
        x = _x;
        y = _y;
        z = _z;
    }
    DEVICE_CALLABLE vector3(const vector2& v, real _z = 0)
    {
        x = v.x;
        y = v.y;
        z = _z;
    }
    DEVICE_CALLABLE vector3(const vector3& v)
    {
        x = v.x;
        y = v.y;
        z = v.z;
    }

    DEVICE_CALLABLE bool isINF() const
    {
        return !isfinite(x) || !isfinite(y) || !isfinite(z);
    }

    DEVICE_CALLABLE real& operator[](int ind)
    {
        return val[ind];
    }
    DEVICE_CALLABLE real operator[](int ind) const
    {
        return val[ind];
    }

    vector2 xx() const { return vector2(x, x); }
    vector2 xy() const { return vector2(x, y); }
    vector2 xz() const { return vector2(x, z); }
    vector2 yx() const { return vector2(y, x); }
    vector2 yy() const { return vector2(y, y); }
    vector2 yz() const { return vector2(y, z); }
    vector2 zx() const { return vector2(z, x); }
    vector2 zy() const { return vector2(z, y); }
    vector2 zz() const { return vector2(z, z); }

    void xy(const vector2& _xy)
    {
        x = _xy.x;
        y = _xy.y;
    }
    void xz(const vector2& _xz)
    {
        x = _xz.x;
        z = _xz.y;
    }
    void yz(const vector2& _yz)
    {
        y = _yz.x;
        z = _yz.y;
    }

    vector3 xxx() const { return vector3(x, x, x); }
    vector3 xxy() const { return vector3(x, x, y); }
    vector3 xxz() const { return vector3(x, x, z); }
    vector3 xyx() const { return vector3(x, y, x); }
    vector3 xyy() const { return vector3(x, y, y); }
    vector3 xyz() const { return vector3(x, y, z); }
    vector3 xzx() const { return vector3(x, z, x); }
    vector3 xzy() const { return vector3(x, z, y); }
    vector3 xzz() const { return vector3(x, z, z); }
    vector3 yxx() const { return vector3(y, x, x); }
    vector3 yxy() const { return vector3(y, x, y); }
    vector3 yxz() const { return vector3(y, x, z); }
    vector3 yyx() const { return vector3(y, y, x); }
    vector3 yyy() const { return vector3(y, y, y); }
    vector3 yyz() const { return vector3(y, y, z); }
    vector3 yzx() const { return vector3(y, z, x); }
    vector3 yzy() const { return vector3(y, z, y); }
    vector3 yzz() const { return vector3(y, z, z); }
    vector3 zxx() const { return vector3(z, x, x); }
    vector3 zxy() const { return vector3(z, x, y); }
    vector3 zxz() const { return vector3(z, x, z); }
    vector3 zyx() const { return vector3(z, y, x); }
    vector3 zyy() const { return vector3(z, y, y); }
    vector3 zyz() const { return vector3(z, y, z); }
    vector3 zzx() const { return vector3(z, z, x); }
    vector3 zzy() const { return vector3(z, z, y); }
    vector3 zzz() const { return vector3(z, z, z); }
    vector3 xyo() const { return vector3(x, y, 0); }
    vector3 xoz() const { return vector3(x, 0, z); }
    vector3 oyz() const { return vector3(0, y, z); }

    DEVICE_CALLABLE vector3 operator+(const vector3& _p) const
    {
        vector3 fp;
        fp.x = x + _p.x;
        fp.y = y + _p.y;
        fp.z = z + _p.z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator+=(const vector3& _p)
    {
        x += _p.x;
        y += _p.y;
        z += _p.z;
        return *this;
    }
    DEVICE_CALLABLE vector3 operator-(const vector3& _p) const
    {
        vector3 fp;
        fp.x = x - _p.x;
        fp.y = y - _p.y;
        fp.z = z - _p.z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator-=(const vector3& _p)
    {
        x -= _p.x;
        y -= _p.y;
        z -= _p.z;
        return *this;
    }
    DEVICE_CALLABLE vector3 operator-() const
    {
        vector3 fp;
        fp.x = -x;
        fp.y = -y;
        fp.z = -z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator*(real s) const
    {
        vector3 fp;
        fp.x = s * x;
        fp.y = s * y;
        fp.z = s * z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator*(const vector3& v) const
    {
        vector3 fp;
        fp.x = v.x * x;
        fp.y = v.y * y;
        fp.z = v.z * z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator*=(const vector3& s)
    {
        x = s.x * x;
        y = s.y * y;
        z = s.z * z;
        return (*this);
    }
    DEVICE_CALLABLE friend vector3 operator*(real s, const vector3& v)
    {
        vector3 fp;
        fp.x = v.x * s;
        fp.y = v.y * s;
        fp.z = v.z * s;
        return fp;
    }
    DEVICE_CALLABLE void operator*=(real s)
    {
        x = s * x;
        y = s * y;
        z = s * z;
    }
    DEVICE_CALLABLE vector3 operator/(real s) const
    {
        vector3 fp;
        fp.x = x / s;
        fp.y = y / s;
        fp.z = z / s;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator/=(real s)
    {
        x = x / s;
        y = y / s;
        z = z / s;
        return (*this);
    }
    DEVICE_CALLABLE vector3 operator/(const vector3& v) const
    {
        vector3 fp;
        fp.x = x / v.x;
        fp.y = y / v.y;
        fp.z = z / v.z;
        return fp;
    }
    DEVICE_CALLABLE vector3 operator/=(const vector3& s)
    {
        x = x / s.x;
        y = y / s.y;
        z = z / s.z;
        return (*this);
    }
    DEVICE_CALLABLE vector3 operator%(const vector3& v) const
    {
        return vector3(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x);
    }
    DEVICE_CALLABLE bool operator==(const vector3& rv) const
    {
        return (fabs(x - rv.x) <= sEPSILON && fabs(y - rv.y) <= sEPSILON && fabs(z - rv.z) <= sEPSILON);
    }
    DEVICE_CALLABLE bool operator!=(const vector3& rv) const
    {
        return (fabs(x - rv.x) > sEPSILON || fabs(y - rv.y) > sEPSILON || fabs(z - rv.z) > sEPSILON);
    }
    DEVICE_CALLABLE bool operator<(const vector3& rv) const
    {
        if (x < rv.x && y < rv.y && z < rv.z)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator<=(const vector3& rv) const
    {
        if (x <= rv.x && y <= rv.y && z <= rv.z)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator>(const vector3& rv) const
    {
        if (x > rv.x && y > rv.y && z > rv.z)
            return true;
        return false;
    }
    DEVICE_CALLABLE bool operator>=(const vector3& rv) const
    {
        if (x >= rv.x && y >= rv.y && z >= rv.z)
            return true;
        return false;
    }
    DEVICE_CALLABLE vector3 flipX() const
    {
        return vector3(-x, y, z);
    }
    DEVICE_CALLABLE vector3 flipY() const
    {
        return vector3(x, -y, z);
    }
    DEVICE_CALLABLE vector3 flipZ() const
    {
        return vector3(x, y, -z);
    }
    DEVICE_CALLABLE real len() const
    {
        return sqrt(x * x + y * y + z * z);
    }
    DEVICE_CALLABLE real length() const
    {
        return sqrt(x * x + y * y + z * z);
    }
    DEVICE_CALLABLE real lenxy() const
    {
        return sqrt(x * x + y * y);
    }
    DEVICE_CALLABLE real sqrlenxy() const
    {
        return (x * x + y * y);
    }
    DEVICE_CALLABLE real lenxz() const
    {
        return sqrt(x * x + z * z);
    }
    DEVICE_CALLABLE real sqrlenxz() const
    {
        return (x * x + z * z);
    }
    DEVICE_CALLABLE real sqrlen() const
    {
        return (x * x + y * y + z * z);
    }
    DEVICE_CALLABLE real len_squared() const
    {
        return (x * x + y * y + z * z);
    }
    DEVICE_CALLABLE real abslen() const
    {
        return abs(x) + abs(y) + abs(z);
    }
    DEVICE_CALLABLE real mean() const
    {
        return ((x) + (y) + (z)) / 3.0;
    }
    DEVICE_CALLABLE real volum() const
    {
        return abs(x) * abs(y) * abs(z);
    }
    // 归一化
    DEVICE_CALLABLE bool normalize()
    {
        real _r = len();
        if (_r > sEPSILON)
        {
            x /= _r;
            y /= _r;
            z /= _r;
            return true;
        }
        return false;
    }
    DEVICE_CALLABLE vector3 normcopy() const
    {
        real _r = len();
        if (_r > sEPSILON)
            return vector3(this->x / _r,
                           this->y / _r,
                           this->z / _r);        
        return vector3(0, 0, 0);
    }
    DEVICE_CALLABLE vector3 normalized() const
    {
        real _r = len();
        if (_r > sEPSILON)
            return vector3(this->x / _r,
                           this->y / _r,
                           this->z / _r);
        return vector3(0, 0, 0);
    }
    DEVICE_CALLABLE real dot(const vector3& v) const
    {
        return x * v.x + y * v.y + z * v.z;
    }
    DEVICE_CALLABLE vector3 crossdot(const vector3& n) const
    {
        const vector3& v = (*this);
        return v - n * v.dot(n);
    }
    DEVICE_CALLABLE vector3 cross(const vector3& v) const
    {
        // Use global handedness setting
        if (g_use_left_handed_system) {
            // Left-handed system
            vector3 n;
            n.x = -(y * v.z - z * v.y);
            n.y = -(z * v.x - x * v.z);
            n.z = -(x * v.y - y * v.x);
            return n;
        } else {
            // Right-handed system
            vector3 n;
            n.x = (y * v.z - z * v.y);
            n.y = (z * v.x - x * v.z);
            n.z = (x * v.y - y * v.x);
            return n;
        }
    }
    DEVICE_CALLABLE vector3 cross_left(const vector3& v) const
    {
        vector3 n;
        // 这里使用了左手顺序！
        n.x = -(y * v.z - z * v.y);
        n.y = -(z * v.x - x * v.z);
        n.z = -(x * v.y - y * v.x);
        return n;
    }
    DEVICE_CALLABLE vector3 cross_right(const vector3& v) const
    {
        vector3 n;
        n.x = (y * v.z - z * v.y);
        n.y = (z * v.x - x * v.z);
        n.z = (x * v.y - y * v.x);
        return n;
    }
    DEVICE_CALLABLE vector3 scale(const vector3& v, real scale) const
    {
        vector3 scaled_v;
        vector3 normalized_v = v.normalized();
        scaled_v = ((*this) + (scale - 1) * ((*this).dot(normalized_v)) * normalized_v);
        return scaled_v;
    }
    DEVICE_CALLABLE vector3 project(const vector3& T) const
    {
        real dotProduct = dot(T);
        real TLengthSquared = T.dot(T);
        if (TLengthSquared > sEPSILON)
        {
            return (dotProduct / TLengthSquared) * T;
        }
        return vector3(0, 0, 0);
    }
    std::string serialise() const
    {
        return std::to_string(x) + "," + std::to_string(y) + "," + std::to_string(z);
    }
    std::string to_string() const
    {
        return std::to_string(x) + "," + std::to_string(y) + "," + std::to_string(z);
    }

    // GUID
    std::size_t hash(int precision_level) const
    {
        std::size_t hashValue = 0;

        if (sizeof(real) == sizeof(real))
        {
            // 保留 precisionLevel 位小数
            real factor = std::pow(10.0f, precision_level);

            // 哈希原点坐标
            hash_combine(hashValue, std::round(x * factor) / factor);
            hash_combine(hashValue, std::round(y * factor) / factor);
            hash_combine(hashValue, std::round(z * factor) / factor);
        }
        return hashValue;
    }
    static vector3 min3(const vector3& a, const vector3& b)
    {
        return vector3(_MIN(a.x, b.x), _MIN(a.y, b.y), _MIN(a.z, b.z));
    }
    static vector3 max3(const vector3& a, const vector3& b)
    {
        return vector3(_MAX(a.x, b.x), _MAX(a.y, b.y), _MAX(a.z, b.z));
    }
    static vector3 rnd(real min = 0, real max = 1)
    {
        return vector3(rrnd(min, max), rrnd(min, max), rrnd(min, max));
    }
    static vector3 rndrad(real r = 1)
    {
        return rnd(-1, 1).normcopy() * r;
    }
    static vector3 lerp(const vector3& v1, const vector3& v2, real t)
    {
        return v1 * (1 - t) + v2 * t;
    }
    static vector3 lerp(const vector3& v1, const vector3& v2, const vector3& t)
    {
        return v1 * (vector3::ONE - t) + v2 * t;
    }
    static real angle(const vector3& a, const vector3& b)
    {
        return std::acos(a.dot(b) / (a.len() * b.len()));
    }
    static real angle(const vector3& a, const vector3& b, const vector3& axis)
    {
        real angle = std::acos(a.dot(b) / (a.len() * b.len()));
        vector3 cross_dir = a.cross(b);
        if (cross_dir.dot(axis) < 0)
        {
            angle = 2 * PI - angle;
        }
        return angle;
    }
};

inline const vector3 vector3::ZERO = vector3(0, 0, 0);
inline const vector3 vector3::ONE = vector3(1, 1, 1);
inline const vector3 vector3::UX = vector3(1, 0, 0);
inline const vector3 vector3::UY = vector3(0, 1, 0);
inline const vector3 vector3::UZ = vector3(0, 0, 1);
inline const vector3 vector3::CENTER = vector3(0, 0, 0);
inline const vector3 vector3::INFINITY3 = vector3(INFINITY, INFINITY, INFINITY);
inline real vector3::sEPSILON = EPSILON;

// **********************************************************************
// 4D vector
// **********************************************************************
struct vector4
{
    static const vector4 ZERO;
    static const vector4 UX;
    static const vector4 UY;
    static const vector4 UZ;
    static const vector4 UW;
    static const vector4 CENTER;
    static real sEPSILON;

    union {
        real val[4];
        struct
        {
            real x;
            real y;
            real z;
            real w;
        };
    };
    DEVICE_CALLABLE vector4()
    {
        x = 0;
        y = 0;
        z = 0;
        w = 0;
    }
    DEVICE_CALLABLE vector4(real _x, real _y, real _z, real _w)
    {
        x = _x;
        y = _y;
        z = _z;
        w = _w;
    }
    DEVICE_CALLABLE vector4(real _x, crvec _v3)
    {
        x = _x;
        y = _v3.x;
        z = _v3.y;
        w = _v3.z;
    }
    DEVICE_CALLABLE vector4(crvec _v3, real _w = 0)
    {
        x = _v3.x;
        y = _v3.y;
        z = _v3.z;
        w = _w;
    }
    DEVICE_CALLABLE explicit vector4(real _v)
    {
        x = _v;
        y = _v;
        z = _v;
        w = _v;
    }
    DEVICE_CALLABLE real& operator[](int ind)
    {
        return val[ind];
    }
    DEVICE_CALLABLE vector3 xyz() const { return vector3(x, y, z); }
    DEVICE_CALLABLE vector3 yzw() const { return vector3(y, z, w); }

    DEVICE_CALLABLE vector4 operator+(const vector4& _p) const
    {
        vector4 fp;
        fp.x = x + _p.x;
        fp.y = y + _p.y;
        fp.z = z + _p.z;
        fp.w = w + _p.w;
        return fp;
    }
    DEVICE_CALLABLE void operator+=(const vector4& _p)
    {
        x += _p.x;
        y += _p.y;
        z += _p.z;
        w += _p.w;
    }
    DEVICE_CALLABLE vector4 operator-(const vector4& _p) const
    {
        vector4 fp;
        fp.x = x - _p.x;
        fp.y = y - _p.y;
        fp.z = z - _p.z;
        fp.w = w - _p.w;
        return fp;
    }
    DEVICE_CALLABLE void operator-=(const vector4& _p)
    {
        x -= _p.x;
        y -= _p.y;
        z -= _p.z;
        w -= _p.w;
    }
    DEVICE_CALLABLE vector4 operator-() const
    {
        vector4 fp;
        fp.x = -x;
        fp.y = -y;
        fp.z = -z;
        fp.w = -w;
        return fp;
    }
    DEVICE_CALLABLE vector4 operator*(real s) const
    {
        vector4 fp;
        fp.x = s * x;
        fp.y = s * y;
        fp.z = s * z;
        fp.w = s * w;
        return fp;
    }
    DEVICE_CALLABLE friend vector4 operator*(real s, const vector4& v)
    {
        vector4 fp;
        fp.x = v.x * s;
        fp.y = v.y * s;
        fp.z = v.z * s;
        fp.w = v.w * s;
        return fp;
    }
    DEVICE_CALLABLE void operator*=(real s)
    {
        x = s * x;
        y = s * y;
        z = s * z;
        w = s * w;
    }
    DEVICE_CALLABLE vector4 operator/(real s) const
    {
        vector4 fp;
        fp.x = x / s;
        fp.y = y / s;
        fp.z = z / s;
        fp.w = w / s;
        return fp;
    }
    DEVICE_CALLABLE void operator/=(real s)
    {
        x = x / s;
        y = y / s;
        z = z / s;
        w = w / s;
    }
    DEVICE_CALLABLE bool operator==(const vector4& rv) const
    {
        return (fabs(x - rv.x) <= EPSILON && fabs(y - rv.y) <= EPSILON && fabs(z - rv.z) <= EPSILON && fabs(w - rv.w) <= EPSILON);
    }
    DEVICE_CALLABLE bool operator!=(const vector4& rv) const
    {
        return (fabs(x - rv.x) > EPSILON || fabs(y - rv.y) > EPSILON || fabs(z - rv.z) > EPSILON || fabs(w - rv.w) > EPSILON);
    }
    DEVICE_CALLABLE real len() const
    {
        return sqrt(x * x + y * y + z * z + w * w);
    }
    DEVICE_CALLABLE real sqrlen() const
    {
        return (x * x + y * y + z * z + w * w);
    }
    DEVICE_CALLABLE real len_squared() const
    {
        return (x * x + y * y + z * z + w * w);
    }
    DEVICE_CALLABLE real normalize()
    {
        real r = len();
        if (r > 1e-5)
        {
            x /= r;
            y /= r;
            z /= r;
            w /= r;
        }
        return r;
    }
    DEVICE_CALLABLE vector4 normcopy()
    {
        real r = len();
        if (r > sEPSILON)
        {
            return vector4(
                this->x / r,
                this->y / r,
                this->z / r,
                this->w / r);
        }
        return vector4(0, 0, 0, 0);
    }
    DEVICE_CALLABLE vector4 normalized()
    {
        real r = len();
        if (r > 0)
        {
            return vector4(
                this->x / r,
                this->y / r,
                this->z / r,
                this->w / r);
        }
        return vector4(0, 0, 0, 0);
    }

    DEVICE_CALLABLE real dot(const vector4& v) const
    {
        return x * v.x + y * v.y + z * v.z + w * v.w;
    }

    // Cross4 computes the four-dimensional cross product of the three vectors
    // U, V and W, in that order. It returns the resulting four-vector.

    DEVICE_CALLABLE vector4 cross(const vector4& V, const vector4& W) const
    {
        vector4 result;
        double A, B, C, D, E, F; // Intermediate Values

        // Calculate intermediate values.

        A = (V.x * W.y) - (V.y * W.x);
        B = (V.x * W.z) - (V.z * W.x);
        C = (V.x * W.w) - (V.w * W.x);
        D = (V.y * W.z) - (V.z * W.y);
        E = (V.y * W.w) - (V.w * W.y);
        F = (V.z * W.w) - (V.w * W.z);

        // Calculate the result-vector components.

        result.x = (y * F) - (z * E) + (w * D);
        result.y = -(x * F) + (z * C) - (w * B);
        result.z = (x * E) - (y * C) + (w * A);
        result.w = -(x * D) + (y * B) - (z * A);

        return result;
    }
};
// **********************************************************************

inline const vector4 vector4::ZERO = vector4(0, 0, 0, 0);
inline const vector4 vector4::UX = vector4(1, 0, 0, 0);
inline const vector4 vector4::UY = vector4(0, 1, 0, 0);
inline const vector4 vector4::UZ = vector4(0, 0, 1, 0);
inline const vector4 vector4::UW = vector4(0, 0, 0, 1);
inline const vector4 vector4::CENTER = vector4(0.5, 0.5, 0.5, 0.5);
inline real vector4::sEPSILON = EPSILON;

// **********************************************************************
// 五维向量
// **********************************************************************
struct vector5
{
    union {
        real val[5];
        struct
        {
            real x;
            real y;
            real z;
            real u;
            real v;
        };
    };
    vector5()
    {
        x = 0;
        y = 0;
        z = 0;
        u = 0;
        v = 0;
    }
    vector5(crvec _v3, real _u = 0, real _v = 0)
    {
        x = _v3.x;
        y = _v3.y;
        z = _v3.z;
        u = _u;
        v = _v;
    }

    vector3 xyz() const { return vector3(x, y, z); }

    real& operator[](int i) { return (&x)[i]; }

    const real& operator[](int i) const { return (&x)[i]; }
};

// **********************************************************************
//							【nD Vector】
//                             多维向量
// **********************************************************************
struct vectorn
{
    std::vector<real> val;

    static const vectorn ZERO;
    static const vectorn ONE;
    static const vectorn CENTER;
    static real sEPSILON;

    real& operator[](int ind)
    {
        if (ind >= val.size())
        { // 自动扩容
            val.resize(ind + 1);
        }
        return val[ind];
    }
    real operator[](int ind) const
    {
        if (ind >= val.size())
        {
            return 0;
        }
        return val[ind];
    }
    vectorn() {}
    vectorn(const std::initializer_list<real>& list)
        : val(list) {}
    explicit vectorn(real v, int size)
        : val(size, v) {}
    explicit vectorn(real v)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] = v;
        }
    }
    vectorn& operator<<(real v)
    {
        val.push_back(v);
        return *this;
    }
    vectorn& operator>>(real& v)
    {
        v = val.back();
        val.pop_back();
        return *this;
    }
    vectorn& operator<<(const vector3& v)
    {
        val.push_back(v.x);
        val.push_back(v.y);
        val.push_back(v.z);
        return *this;
    }
    vectorn& operator>>(vector3& v)
    {
        v.x = val.back();
        val.pop_back();
        v.z = val.back();
        val.pop_back();
        v.z = val.back();
        val.pop_back();
        return *this;
    }

    void operator=(const vector3& v)
    {
        val[0] = v.x;
        val[1] = v.y;
        val[2] = v.z;
    }
    vectorn operator+(const vectorn& _p) const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = val[i] + _p[i];
        }
        return fp;
    }
    void operator+=(const vectorn& _p)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] += _p[i];
        }
    }
    vectorn operator-(const vectorn& _p) const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = val[i] - _p[i];
        }
        return fp;
    }
    void operator-=(const vectorn& _p)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] -= _p[i];
        }
    }
    vectorn operator-() const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = -val[i];
        }
        return fp;
    }
    vectorn operator*(const vectorn& _p) const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = val[i] * _p[i];
        }
        return fp;
    }
    void operator*=(const vectorn& _p)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] *= _p[i];
        }
    }
    vectorn operator*(real s) const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = val[i] * s;
        }
        return fp;
    }
    void operator*=(real s)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] *= s;
        }
    }
    friend vectorn operator*(real s, vectorn& v)
    {
        vectorn fp;
        for (int i = 0; i < v.val.size(); i++)
        {
            fp[i] = v[i] * s;
        }
        return fp;
    }
    vectorn operator/(real s) const
    {
        vectorn fp;
        for (int i = 0; i < val.size(); i++)
        {
            fp[i] = val[i] / s;
        }
        return fp;
    }
    void operator/=(real s)
    {
        for (int i = 0; i < val.size(); i++)
        {
            val[i] /= s;
        }
    }
    bool operator==(const vectorn& v) const
    {
        if (val.size() != v.val.size())
            return false;
        bool ret = true;
        for (int i = 0; i < val.size(); i++)
        {
            ret &= (fabs(val[i] - v.val[i]) <= 1e-5);
            if (!ret)
                break;
        }
        return ret;
    }
    bool operator!=(const vectorn& v) const
    {
        if (val.size() != v.val.size())
            return true;
        bool ret = false;
        for (int i = 0; i < val.size(); i++)
        {
            ret |= (fabs(val[i] - v.val[i]) <= 1e-5);
            if (ret)
                break;
        }
        return ret;
    }
    int dim() const
    {
        return val.size();
    }
    real len() const
    {
        real sqred = 0;
        for (int i = 0; i < val.size(); i++)
        {
            sqred += val[i] * val[i];
        }
        return sqrt(sqred);
    }
    real sqrlen() const
    {
        real sqred = 0;
        for (int i = 0; i < val.size(); i++)
        {
            sqred += val[i] * val[i];
        }
        return sqred;
    }
    void normalize()
    {
        real r = len();
        if (r > 0)
        {
            (*this) /= r;
        }
    }
    vectorn normcopy() const
    {
        real r = len();
        if (r > 0)
        {
            return (*this) / r;
        }
        return vectorn::ZERO;
    }
    real dot(const vectorn& v) const
    {
        // ASSERT(val.size() == v.val.size());
        real sum = 0;
        for (int i = 0; i < val.size(); i++)
        {
            sum += val[i] * v.val[i];
        }
        return sum;
    }
    size_t hash() const
    {
        size_t xorResult = 0;
        for (const auto& value : val)
        {
            xorResult ^= static_cast<size_t>(value);
        }
        return xorResult;
    }
    void dump() const
    {
        std::cout << "vectorn: [";
        for (size_t i = 0; i < val.size(); ++i)
        {
            if (val[i] != 0)
            {
                std::cout << i << ":" << val[i];
                if (i < val.size() - 1)
                {
                    std::cout << ", ";
                }
            }
        }
        std::cout << "]\n"
                  << std::endl;
    }
};
// **********************************************************************

inline const vectorn vectorn::ZERO = vectorn(0);
inline const vectorn vectorn::ONE = vectorn(1);
inline const vectorn vectorn::CENTER = vectorn(0.5);
/**************************************************************************
						 【四元数】

	四元数是在复数基础上的扩展,单位四元数用于旋转操作，向量是源自于四元数，
	不过二者有差别。目前四元数跟向量之间的关系以及应用存在着争议。

	*  *  *  *  *  *  *  *  *  详解  *  *  *  *  *  *  *  *  *  *  *  *  * 
	类似于复数，四元数也拥有指数形式：e^q，结果也是一个四元数： q = e^q,
	在底层物理里应了规范变换，跟坐标系变换有一些不同，规范变换更加
	侧重相位拥有时间属性，坐标系变换偏向于空间的变换以及曲率等特征提取。

	四元数存在归一化(normalise)，共轭(conj)，求逆(inverse)，乘除法等操作，
	还规定了单位一（ONE).

**************************************************************************/
struct  quaternion
{
	static const quaternion ONE;
	static const quaternion UX;
	static const quaternion UY;
	static const quaternion UZ;

	real w = 1, x = 0, y = 0, z = 0;

	//-----------------------------------------------------------------------
	quaternion() { }
	quaternion(
		real fW,
		real fX, real fY, real fZ)
	{
		w = fW;
		x = fX;
		y = fY;
		z = fZ;
	}
	quaternion(real pitch, real yaw, real roll)
	{
		from_eulers(pitch, yaw, roll);
	}
	quaternion(const vector3& pyr)
	{
		from_eulers(pyr.x, pyr.y, pyr.z);
	}
	quaternion(const quaternion& rkQ)
	{
		w = rkQ.w;
		x = rkQ.x;
		y = rkQ.y;
		z = rkQ.z;
	}
	quaternion(real rfAngle, const vector3& rkAxis)
	{
		ang_axis(rfAngle, rkAxis);
	}	
	quaternion(const vec3& v1, const vec3& v2)
	{
		from_vectors(v1, v2);
	}

	//-----------------------------------------------------------------------
	bool is_finite() const 
	{
		return std::isfinite(x) && std::isfinite(y) && std::isfinite(z) && std::isfinite(w);
	}

	//-----------------------------------------------------------------------
	quaternion operator+ (const quaternion& rkQ) const
	{
		return quaternion(w + rkQ.w, x + rkQ.x, y + rkQ.y, z + rkQ.z);
	}

	quaternion operator- (const quaternion& rkQ) const
	{
		return quaternion(w - rkQ.w, x - rkQ.x, y - rkQ.y, z - rkQ.z);
	}
	quaternion operator - () const
	{
		quaternion q;
		q.x = -x;
		q.y = -y;
		q.z = -z;
		q.w = -w;
		return q;
	}

	//-----------------------------------------------------------------------
	vector3 operator* (const vector3& v) const
	{
		// nVidia SDK implementation
		vector3 uv, uuv;
		vector3 qvec(x, y, z);
		uv = qvec.cross(v);
		uuv = qvec.cross(uv);
		uv = uv * (2.0f * w);
		uuv = uuv * 2.0f;

		return v + uv + uuv;
	}
	vector3 friend operator* (const vector3& v, const quaternion& q)
	{
		return q * v;
	}
	void friend operator*= (vector3& v, const quaternion& q)
	{
		v = q * v;
	}
	// 这是是Ogre引擎的实现 (习惯上 父->子 顺序)
	quaternion operator*(const quaternion& rkQ) const
	{
		// NOTE:  Multiplication is not generally commutative, so in most
		// cases p*q != q*p.

		return quaternion
		(
			w * rkQ.w - x * rkQ.x - y * rkQ.y - z * rkQ.z,
			w * rkQ.x + x * rkQ.w + y * rkQ.z - z * rkQ.y,
			w * rkQ.y + y * rkQ.w + z * rkQ.x - x * rkQ.z,
			w * rkQ.z + z * rkQ.w + x * rkQ.y - y * rkQ.x
		);
	}
	void operator*= (const quaternion& rkQ)
	{
		(*this) = (*this) * rkQ;
	}
	quaternion operator* (real fScalar) const
	{
		return quaternion(fScalar * w, fScalar * x, fScalar * y, fScalar * z);
	}
	quaternion friend operator* (real fScalar, const quaternion& rkQ)
	{
		return quaternion(fScalar * rkQ.w, fScalar * rkQ.x, fScalar * rkQ.y,
			fScalar * rkQ.z);
	}

	//-----------------------------------------------------------------------
	quaternion operator / (real fScalar) const
	{
		return quaternion(w / fScalar, x / fScalar, y / fScalar, z / fScalar);
	}
	void operator /= (real fScalar)
	{
		w /= fScalar;
		x /= fScalar;
		y /= fScalar;
		z /= fScalar;
	}
	quaternion operator / (const quaternion& q) const
	{
		return (*this) * q.conjcopy();
	}
	vector3 friend operator / (const vector3& v, const quaternion& q)
	{
		return q.conjcopy() * v;
	}

	//-----------------------------------------------------------------------
	bool operator == (const quaternion& rkQ) const
	{
		return (fabs(w - rkQ.w) < EPSILON) &&
			(fabs(x - rkQ.x) < EPSILON) &&
			(fabs(y - rkQ.y) < EPSILON) &&
			(fabs(z - rkQ.z) < EPSILON);
	}
	//-----------------------------------------------------------------------
	bool operator != (const quaternion& rkQ) const
	{
		return !(*this == rkQ);
	}
	//-----------------------------------------------------------------------
	real dot(const quaternion& rkQ) const
	{
		return w * rkQ.w + x * rkQ.x + y * rkQ.y + z * rkQ.z;
	}
	//-----------------------------------------------------------------------
	real length() const
	{
		return sqrt(w * w + x * x + y * y + z * z);
	}
	//-----------------------------------------------------------------------
	vec3 xyz() const
	{
		return vec3(x, y, z);
	}
	// ============================================================================
	// 轴角表示相关函数
	// ============================================================================

	// 获取旋转轴（归一化）
	vec3 axis() const
	{
		return vec3(x, y, z).normcopy();
	}

	// 获取旋转角度（弧度）
	real angle() const
	{
		if (w >= 1.0)
			return 0.0;
		if (w <= -1.0)
			return PI;
		real ang = acos(w) * 2;
		if (ang > PI)
			return ang - PI * 2; // 归一化到 [-π, π]
		if (ang < -PI)
			return ang + PI * 2;
		return ang;
	}

	// 设置旋转角度，保持轴不变
	void set_angle(real ang)
	{
		ang_axis(ang, axis());
	}

	// 同时获取旋转角度和轴
	void to_angle_axis(real& out_angle, vec3& out_axis) const
	{
		out_angle = angle();
		out_axis = axis();
	}

	// 计算到另一个四元数的角度差
	real angle_to(const quaternion& q) const
	{
		real d = dot(q);
		return acos(d * d * 2 - 1);
	}
	//-----------------------------------------------------------------------
	quaternion normalize(void)
	{
		real len = length();
		if (len != 0)
		{
			real factor = 1.0f / (len);
			*this = *this * factor;
		}
		return *this;
	}
	quaternion normalized(void) const
	{
		real len = length();
		if (len == 0)
		{
			return quaternion::ONE;
		}
		return (*this) / len;
	}
	//-----------------------------------------------------------------------
	// 共轭
	void conj()
	{
		this->x = -x; this->y = -y; this->z = -z;
	}
	quaternion conjcopy() const
	{
		quaternion q;
		q.w = w;
		q.x = -x; q.y = -y; q.z = -z;
		return q;
	}
	//-----------------------------------------------------------------------
	// 求逆
	quaternion inverse() const {
		real lenSquared = w * w + x * x + y * y + z * z;
		if (lenSquared != 0) {
			real factor = 1.0f / lenSquared;
			return conjcopy() * factor;
		}
		return quaternion::ONE;
	}
	//-----------------------------------------------------------------------
	// 指数上运算
	quaternion exp() const
	{
		real r = length();
		vec3 v(x, y, z);
		real th = v.len();
		vec3 n = v.normcopy();
		vec3 qv = n * (r * sin(th));
		return quaternion(r * cos(th), qv.x, qv.y, qv.z);
	}
	friend quaternion exp(const quaternion& q)
	{
		real r = q.length();
		vec3 v(q.x, q.y, q.z);
		real th = v.len();
		vec3 n = v.normcopy();
		vec3 qv = n * (r * sin(th));
		return quaternion(r * cos(th), qv.x, qv.y, qv.z);
	}
	quaternion log() const {
		quaternion src = *this;
		vec3 src_v = src.axis() * src.angle();
		return quaternion(src_v.x, src_v.y, src_v.z, 0);
	}
	// 指数运算（注意运算符的优先级）
	quaternion operator ^ (int n) const
	{
		quaternion ret = *this;
		for (int i = 1; i < n; i++)
		{
			ret = ret * (*this);
		}
		return ret;
	}
	quaternion operator ^ (real t)
	{
		return slerp(t, quaternion::ONE, *this, false);
	}
	// ============================================================================
	// 旋转操作：绕轴旋转
	// ============================================================================

	// 绕X轴旋转指定角度
	void rotate_x(real angle)
	{
		quaternion qx(angle, vec3::UX);
		(*this) = (*this) * qx;
	}

	// 绕Y轴旋转指定角度
	void rotate_y(real angle)
	{
		quaternion qy(angle, vec3::UY);
		(*this) = (*this) * qy;
	}

	// 绕Z轴旋转指定角度
	void rotate_z(real angle)
	{
		quaternion qz(angle, vec3::UZ);
		(*this) = (*this) * qz;
	}

	//-----------------------------------------------------------------------
	// 从两个向量创建旋转（v1 旋转到 v2）
	// v1, v2 可以是非单位向量
	#define fromvectors	from_vectors		// 别名
	quaternion from_vectors(const vec3& v1, const vec3& v2)
	{
		real eps = c_tor_dis_level2;		// 误差等级
		if (fabs(v1.x - v2.x) <= eps && fabs(v1.y - v2.y) <= eps && fabs(v1.z - v2.z) <= eps)
		{
			(*this) = quaternion::ONE;
		}
		else
		{
			real dot = v1.dot(v2);
			if (std::abs(dot + 1.0) < eps)	// 处理180度的情况
			{
				vec3 ax;
				vec3 uz = vec3::UZ;
				if (std::abs(v1.x) < eps && std::abs(v1.y) < eps)
					uz = -vec3::UX;
				ax = uz.cross(v1).normalized();
				ang_axis(PI, ax.normalized());
			}
			else if (dot > -1.0 + eps && dot <= 1.0 - eps) // 处理一般情况
			{
				vec3 axis = v1.cross(v2).normalized();
				real angle = std::acos(dot);
				ang_axis(angle, axis);
			}
		}
		return (*this);
	}
	//-----------------------------------------------------------------------
	// 角度，轴向定义
	quaternion ang_axis(real rfAngle, const vec3& rkAxis)
	{
		// assert:  axis[] is unit length
		//
		// The quaternion representing the rotation is
		//   q = cos(A/2)+sin(A/2)*(x*i+y*j+z*k)

		real fHalfAngle(0.5 * rfAngle);
		real fSin = sin(fHalfAngle);
		w = cos(fHalfAngle);
		x = fSin * rkAxis.x;
		y = fSin * rkAxis.y;
		z = fSin * rkAxis.z;

		return (*this);
	}
	//-----------------------------------------------------------------------
	#define fromeulers	from_eulers // 别名
	void from_eulers(real roll, real pitch, real yaw)
	{
		real t0 = cos(yaw * 0.5);
		real t1 = sin(yaw * 0.5);
		real t2 = cos(roll * 0.5);
		real t3 = sin(roll * 0.5);
		real t4 = cos(pitch * 0.5);
		real t5 = sin(pitch * 0.5);

		w = t2 * t4 * t0 + t3 * t5 * t1;
		x = t3 * t4 * t0 - t2 * t5 * t1;
		y = t2 * t5 * t0 + t3 * t4 * t1;
		z = t2 * t4 * t1 - t3 * t5 * t0;
	}
	//-----------------------------------------------------------------------
	// roll, pitch, yaw
	#define toeulers	to_eulers // 别名
	vec3 to_eulers() const
	{
		vec3 v;

		real epsilon = 0.00001f;
		real halfpi = 0.5 * PI;

		real temp = 2 * (y * z - x * w);
		if (temp >= 1 - epsilon)
		{
			v.x = halfpi;
			v.y = -atan2(y, w);
			v.z = -atan2(z, w);
		}
		else if (-temp >= 1 - epsilon)
		{
			v.x = -halfpi;
			v.y = -atan2(y, w);
			v.z = -atan2(z, w);
		}
		else
		{
			v.x = asin(temp);
			v.y = -atan2(x * z + y * w, 0.5 - x * x - y * y);
			v.z = -atan2(x * y + z * w, 0.5 - x * x - z * z);
		}
		return v;
	}
	void to_eulers(real& roll, real& pitch, real& yaw) const
	{
		real sinr_cosp = 2 * (w * x + y * z);
		real cosr_cosp = 1 - 2 * (x * x + y * y);
		roll = atan2(sinr_cosp, cosr_cosp);

		real sinp = 2 * (w * y - z * x);
		if (abs(sinp) >= 1)
			pitch = copysign(PI / 2, sinp);
		else
			pitch = asin(sinp);

		real siny_cosp = 2 * (w * z + x * y);
		real cosy_cosp = 1 - 2 * (y * y + z * z);
		yaw = atan2(siny_cosp, cosy_cosp);
	}
	//-----------------------------------------------------------------------
	static quaternion slerp(const quaternion& qa, const quaternion& qb, real t) {
		// quaternion to return
		quaternion qm;
		// Calculate angle between them.
		real cosHalfTheta = qa.w * qb.w + qa.x * qb.x + qa.y * qb.y + qa.z * qb.z;
		// if qa=qb or qa=-qb then theta = 0 and we can return qa
		if (abs(cosHalfTheta) >= 1.0) {
			qm.w = qa.w; qm.x = qa.x; qm.y = qa.y; qm.z = qa.z;
			return qm;
		}
		// Calculate temporary values.
		real halfTheta = acos(cosHalfTheta);
		real sinHalfTheta = sqrt(1.0 - cosHalfTheta * cosHalfTheta);
		// if theta = 180 degrees then result is not fully defined
		// we could rotate around any axis normal to qa or qb
		if (fabs(sinHalfTheta) < 0.001) { // fabs is floating point absolute
			qm.w = (qa.w * 0.5 + qb.w * 0.5);
			qm.x = (qa.x * 0.5 + qb.x * 0.5);
			qm.y = (qa.y * 0.5 + qb.y * 0.5);
			qm.z = (qa.z * 0.5 + qb.z * 0.5);
			return qm;
		}
		real ratioA = sin((1 - t) * halfTheta) / sinHalfTheta;
		real ratioB = sin(t * halfTheta) / sinHalfTheta;
		//calculate Quaternion.
		qm.w = (qa.w * ratioA + qb.w * ratioB);
		qm.x = (qa.x * ratioA + qb.x * ratioB);
		qm.y = (qa.y * ratioA + qb.y * ratioB);
		qm.z = (qa.z * ratioA + qb.z * ratioB);
		return qm;
	}
	//-----------------------------------------------------------------------
	static quaternion slerp(real fT, const quaternion& rkP,
		const quaternion& rkQ, bool shortestPath)
	{
		const real msEpsilon = 1e-03;
		real fCos = rkP.dot(rkQ);
		quaternion rkT;

		// Do we need to invert rotation?
		if (fCos < 0.0f && shortestPath)
		{
			fCos = -fCos;
			rkT = -rkQ;
		}
		else
		{
			rkT = rkQ;
		}

		if (fabs(fCos) < 1 - msEpsilon)
		{
			// Standard case (slerp)
			real fSin = sqrt(1 - (fCos * fCos));
			real fAngle = atan2(fSin, fCos);
			real fInvSin = 1.0f / fSin;
			real fCoeff0 = sin((1.0f - fT) * fAngle) * fInvSin;
			real fCoeff1 = sin(fT * fAngle) * fInvSin;
			return fCoeff0 * rkP + fCoeff1 * rkT;
		}
		else
		{
			// There are two situations:
			// 1. "rkP" and "rkQ" are very close (fCos ~= +1), so we can do a linear
			//    interpolation safely.
			// 2. "rkP" and "rkQ" are almost inverse of each other (fCos ~= -1), there
			//    are an infinite number of possibilities interpolation. but we haven't
			//    have method to fix this case, so just use linear interpolation here.
			quaternion t = (1.0f - fT) * rkP + fT * rkT;
			// taking the complement requires renormalisation
			t.normalize();
			return t;
		}
	}
	//-----------------------------------------------------------------------
	static quaternion nlerp(real fT, const quaternion& rkP,
		const quaternion& rkQ, bool shortestPath)
	{
		quaternion result;
		real fCos = rkP.dot(rkQ);
		if (fCos < 0.0f && shortestPath)
		{
			result = rkP + fT * ((-rkQ) - rkP);
		}
		else
		{
			result = rkP + fT * (rkQ - rkP);
		}
		result.normalize();
		return result;
	}
	//-----------------------------------------------------------------------
	quaternion spherical_cubic_interpolate(const quaternion& p_b, const quaternion& p_pre_a, const quaternion& p_post_b, const real& p_weight) const {

		quaternion from_q = *this;
		quaternion pre_q = p_pre_a;
		quaternion to_q = p_b;
		quaternion post_q = p_post_b;

		// Align flip phases.
		from_q = from_q.normalized();
		pre_q = pre_q.normalized();
		to_q = to_q.normalized();
		post_q = post_q.normalized();

		// Flip quaternions to shortest path if necessary.
		bool flip1 = sign(from_q.dot(pre_q));
		pre_q = flip1 ? -pre_q : pre_q;
		bool flip2 = sign(from_q.dot(to_q));
		to_q = flip2 ? -to_q : to_q;
		bool flip3 = flip2 ? to_q.dot(post_q) <= 0 : sign(to_q.dot(post_q));
		post_q = flip3 ? -post_q : post_q;

		// Calc by Expmap in from_q space.
		quaternion ln_from = quaternion(0, 0, 0, 0);
		quaternion ln_to = (from_q.conjcopy() * to_q).log();
		quaternion ln_pre = (from_q.conjcopy() * pre_q).log();
		quaternion ln_post = (from_q.conjcopy() * post_q).log();
		quaternion ln = quaternion(0, 0, 0, 0);
		ln.x = cubic_interpolate(ln_from.x, ln_to.x, ln_pre.x, ln_post.x, p_weight);
		ln.y = cubic_interpolate(ln_from.y, ln_to.y, ln_pre.y, ln_post.y, p_weight);
		ln.z = cubic_interpolate(ln_from.z, ln_to.z, ln_pre.z, ln_post.z, p_weight);
		quaternion q1 = from_q * ln.exp();

		// Calc by Expmap in to_q space.
		ln_from = (to_q.conjcopy() * from_q).log();
		ln_to = quaternion(0, 0, 0, 0);
		ln_pre = (to_q.conjcopy() * pre_q).log();
		ln_post = (to_q.conjcopy() * post_q).log();
		ln = quaternion(0, 0, 0, 0);
		ln.x = cubic_interpolate(ln_from.x, ln_to.x, ln_pre.x, ln_post.x, p_weight);
		ln.y = cubic_interpolate(ln_from.y, ln_to.y, ln_pre.y, ln_post.y, p_weight);
		ln.z = cubic_interpolate(ln_from.z, ln_to.z, ln_pre.z, ln_post.z, p_weight);
		quaternion q2 = to_q * ln.exp();

		// To cancel error made by Expmap ambiguity, do blends.
		return quaternion::slerp(q1, q2, p_weight);
	}
};
// **********************************************************************

inline const quaternion quaternion::ONE = quaternion(1, 0, 0, 0);
inline const quaternion quaternion::UX = quaternion(1, vec3::UX);
inline const quaternion quaternion::UY = quaternion(1, vec3::UY);
inline const quaternion quaternion::UZ = quaternion(1, vec3::UZ);
/**
 *					【基础向量数学函数库】
 *
 *			本库提供向量和坐标变换相关的基础数学函数，包括：
 *			- 向量基本运算（点积、叉积、归一化等）
 *			- 向量关系（角度、距离、投影等）
 *			- 辅助工具函数（插值、融合、平滑等）
 */

// ============================================================================
// 向量分量运算
// ============================================================================

// 返回两个向量各分量的最小值组成的新向量
inline vec3 _MINV(crvec a, crvec b) { return vec3(_MIN(a.x, b.x), _MIN(a.y, b.y), _MIN(a.z, b.z)); }

// 返回两个向量各分量的最大值组成的新向量
inline vec3 _MAXV(crvec a, crvec b) { return vec3(_MAX(a.x, b.x), _MAX(a.y, b.y), _MAX(a.z, b.z)); }

// 对向量各分量向上取整
inline vec3 _CEIL(crvec a) { return vec3(std::ceil(a.x), std::ceil(a.y), std::ceil(a.z)); }

// ============================================================================
// 向量比较与判断
// ============================================================================

// 检查两个三维向量是否在误差范围内相等
inline bool equal(const vec3& v1, const vec3& v2, real eps = EPSILON)
{
	return (fabs(v1.x - v2.x) <= eps && fabs(v1.y - v2.y) <= eps && fabs(v1.z - v2.z) <= eps);
}

// 同 equal 函数（别名）
inline bool check_equal(const vec3& v1, const vec3& v2, real eps = EPSILON)
{
	return (fabs(v1.x - v2.x) <= eps && fabs(v1.y - v2.y) <= eps && fabs(v1.z - v2.z) <= eps);
}

// ============================================================================
// 向量正交基构建
// ============================================================================

// 计算给定三维向量的两个垂直向量，存储在vx和vy中
inline void v2vxvy(const vec3& v, vec3& vx, vec3& vy)
{
	vec3 uz = vec3::UZ;
	// 如果v的x和y分量都接近于0，则取uz为垂直向量
	if (v.x < EPSILON && v.x > -EPSILON && v.y < EPSILON && v.y > -EPSILON)
	{
		uz = vec3::UX;
	}
	vx = uz.cross(v); vx.normalize(); // 计算vx为uz和v的叉乘，并归一化
	vy = v.cross(vx); vy.normalize(); // 计算vy为v和vx的叉乘
}

// 计算给定三维向量的两个垂直向量，存储在vx和vy中
inline void vz2vxvy(const vec3& v, vec3& vx, vec3& vy)
{
	vec3 uy = vec3::UY;
	// 如果v的x和z分量都接近于0，则取uy为垂直向量
	if (v.x < EPSILON && v.x > -EPSILON && v.z < EPSILON && v.z > -EPSILON)
	{
		uy = vec3::UZ;
	}
	vx = v.cross(uy); vx.normalize(); // 计算vx为v和uy的叉乘，并归一化
	vy = vx.cross(v); // 计算vy为vx和v的叉乘
}

// 计算给定三维向量的一个垂直向量，存储在vy中，vx作为参数传入
inline void vz2vxvy(const vec3& v, const vec3& vx, vec3& vy)
{
	vec3 uy = vec3::UY;
	// 如果v的x和z分量都接近于0，则取uy为垂直向量
	if (v.x < EPSILON && v.x > -EPSILON && v.z < EPSILON && v.z > -EPSILON)
	{
		uy = vec3::UZ;
	}
	vy = vx.cross(v); // 计算vy为vx和v的叉乘
}

// 计算给定二维向量的一个垂直向量
inline vec3 v2vx(const vec3& v)
{
	vec3 uz = vec3::UZ;
	// 如果v的x和y分量都接近于0，则取uz为垂直向量
	if (v.x < EPSILON && v.x > -EPSILON && v.y < EPSILON && v.y > -EPSILON)
	{
		uz = vec3::UX;
	}
	vec3 vx = uz.cross(v); vx.normalize(); // 计算vx为uz和v的叉乘，并归一化
	return vx;
}
// ============================================================================
// 向量变换与缩放
// ============================================================================

// 将向量v相对于中心点o进行缩放，缩放因子为s
inline vec3 scaleby(crvec v, crvec o, real s)
{
	return (v - o) * s + o;
}

// ============================================================================
// 数值工具函数
// ============================================================================

// 向下取整（整数除法）
inline int floori(real value)
{
	return (value >= 0 ? (int)value : (int)value - 1);
}

// 平滑插值曲线（Perlin噪声使用）: 6x^5 - 15x^4 + 10x^3
inline real fade(real x)
{
	return (x * x * x * (x * (6 * x - 15) + 10));
}

// ============================================================================
// 向量点积与叉积运算
// ============================================================================

// 计算两个二维向量的点积
inline real dot(real x1, real y1, real x2, real y2)
{
	return x1 * x2 + y1 * y2;
}

// 计算两个三维向量的点积
inline real dot(crvec v1, crvec v2)
{
	return v1.dot(v2);
}
inline real dot3(crvec v1, crvec v2)
{
	return v1.dot(v2);
}

// 计算三维向量的点积
inline real dot2(crvec v)
{
	return v.dot(v);
}

// 计算两个三维向量的叉积
inline vec3 cross(crvec v1, crvec v2)
{
	return v1.cross(v2);
}
inline vec3 cross_right(crvec v1, crvec v2)
{
    return v1.cross_right(v2);
}
inline vec3 cross_norm(crvec v1, crvec v2)
{
	return v1.normalized().cross(v2.normalized()).normalized();
}
inline real cross(crvec p1, crvec p2, crvec p3)
{
	return (p2.y - p1.y) * (p3.z - p1.z) - (p2.z - p1.z) * (p3.y - p1.y) +
		(p2.z - p1.z) * (p3.x - p1.x) - (p2.x - p1.x) * (p3.z - p1.z) +
		(p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x);
}
inline vec3 crossdot(const vec3& v, const vec3& n)
{
	return v - n * v.dot(n);
}
// ============================================================================
// 符号与阶跃函数
// ============================================================================
// 注意: sign 函数已在文件开头定义，这里不再重复定义

// 返回向量各分量的符号
inline vec3 sign(crvec v)
{
	return vec3(sign(v.x), sign(v.y), sign(v.z));
}

// 阶跃函数: x < edge 返回 0, 否则返回 1
inline real step(real edge, real x) {
	return x < edge ? 0.0 : 1.0;
}

// 向量版本的阶跃函数
inline vec3 step(crvec edge, crvec v) {
	return vec3(
		v.x < edge.x ? 0.0 : 1.0,
		v.y < edge.y ? 0.0 : 1.0,
		v.z < edge.z ? 0.0 : 1.0);
}

// ============================================================================
// 向量长度与距离计算
// ============================================================================

// 计算实数的倒数平方根
inline real inversesqrt(real v)
{
	return 1.0 / sqrt(v);
}
inline real length_squared(crvec p)
{
	return p.len_squared();
}

// 计算三维向量的长度/距离
inline real length(crvec p)
{
	return p.len();
}
inline real length(crvec a, crvec b)
{
	return (a - b).len();
}
inline real distance(crvec a, crvec b)
{
	return (a - b).len();
}
inline real manhattan_distance(crvec a, crvec b)
{
	return std::abs(a.x - b.x) + std::abs(a.y - b.y) + std::abs(a.z - b.z);
}
inline vec3 abs(crvec p)
{
	return vec3(::abs(p.x),::abs(p.y),::abs(p.z));
}

// 将给定的三维向量归一化
inline vec3 normalize(crvec p)
{
	return p.normcopy();
}
inline vec3 normalize(crvec a, crvec b)
{
	return normalize(b - a);
}
inline vec3 normalize(crvec a, crvec b, crvec c)
{
	return cross(b - a, c - a).normcopy();
}

// 混合两个实数h1和h2，使用alpha和power作为参数
extern real blend(real h1, real h2, real alpha, real power);

// ============================================================================
// 插值与平滑函数
// ============================================================================

// 平滑步进函数（Hermite插值）: 在[a, b]区间内平滑过渡
inline real smoothstep(real a, real b, real s)
{
	real t = blend(0.0f, 1.0f, (s - a) / (b - a), 0);
	return t * t * (3.0 - 2.0 * t);
}

// ============================================================================
// 向量夹角计算
// ============================================================================

// 计算两个三维向量的夹角（弧度），自动归一化
inline real vv_angle(const vec3& a, const vec3& b) {
	real x = dot(a, b) / (a.len() * b.len());
	if (std::isnan(x))
	{
		return std::numeric_limits<real>::quiet_NaN();
	}
	if (x > 1.0)
		x = 1.0;
	else if (x < -1.0)
		x = -1.0;
	return std::acos(x);
}

// 计算两个归一化向量的夹角（假定输入已归一化）
inline real vv_angle_norm(const vec3& a, const vec3& b) {
	return std::acos(dot(a, b));
}

// 计算两个向量在指定轴平面上的有向夹角（带符号）
inline real vv_angle(const vec3& a, const vec3& b, const vec3& axis) {
	real angle = vv_angle(a, b);
	vec3 cross_dir = cross(a, b);
	if (dot(cross_dir, axis) < 0) {
		angle = 2 * PI - angle;
	}
	return angle;
}
inline real vv_angleEX(vec3 a, vec3 b, const vec3& axis) {
	a = a.crossdot(axis);
	b = b.crossdot(axis);
	real angle = vv_angle(a, b);
	vec3 cross_dir = cross(a, b);
	if (dot(cross_dir, axis) < 0) {
		angle = 2 * PI - angle;
	}
	return angle;
}
inline real angle_between(const vec3& a, const vec3& b, const vec3& c) {
	vec3 ab = b - a;
	vec3 ac = c - a;
	real dot_product = ab.dot(ac);
	real length_ab = ab.length();
	real length_ac = ac.length();
	return acos(dot_product / (length_ab * length_ac)); // Returns the angle in radians
}

// 计算两个三维向量的夹角，使用给定的轴进行计算，通过交叉点乘法进行优化
inline real vv_angle_crossdot(vec3 a, vec3 b, const vec3& axis) {
	a = a.crossdot(axis);
	b = b.crossdot(axis);
	real angle = vv_angle(a, b);
	vec3 cross_dir = cross(a, b);
	if (dot(cross_dir, axis) < 0) {
		angle = 2 * PI - angle;
	}
	return angle;
}

// 计算两个三维向量的中心点，使用给定的轴进行计算
inline vec3 vv_center(const vec3& v1, const vec3& v2, const vec3& axis)
{
	real d12 = (v1 - v2).len();
	real ang12 = vv_angle(v1, v2, axis);
	real R = d12 / ::sqrt(2 * (1 - cos(ang12)));

	//vec3 vv = v1.cross(axis).normcopy();
	return - v1 * R;
}

// 返回三维向量中的最大分量
inline real max_elem(const vec3& v) {
	return _MAX(v.x, _MAX(v.y, v.z));
}

// 返回三维向量中的最小分量
inline real min_elem(const vec3& v) {
	return _MIN(v.x, _MIN(v.y, v.z));
}/**					【基础向量数学】
*
*/

// 返回两个二维向量中每个分量较小的值
inline vec2 _MINV(crvec2 a, crvec2 b) { return vec2(_MIN(a.x, b.x), _MIN(a.y, b.y)); }

// 返回两个二维向量中每个分量较大的值
inline vec2 _MAXV(crvec2 a, crvec2 b) { return vec2(_MAX(a.x, b.x), _MAX(a.y, b.y)); }

// 计算两个二维向量的点积
inline real dot(crvec2 v1, crvec2 v2)
{
	return v1.dot(v2);
}

// 计算二维向量的长度
inline real length(crvec2 p)
{
	return p.len();
}

// 计算两个二维向量的距离
inline real distance(crvec2 v1, crvec2 v2)
{
    return (v2 - v1).len();
}

// 返回单位向量，即将向量归一化
inline vec2 normalize(crvec2 v)
{
    return v.normalized();
}

// 向下取整，返回一个由每个分量向下取整得到的新向量
inline vec2 floor(crvec2 v)
{
    return vec2(std::floor(v.x), std::floor(v.y));
}

// 计算分数部分，返回一个由每个分量的分数部分得到的新向量
inline vec2 fract(crvec2 v)
{
    return vec2(v.x - std::floor(v.x), v.y - std::floor(v.y));
}

// 计算取余，返回一个由每个分量与给定值取余得到的新向量
inline vec2 mod(crvec2 v, real m)
{
    return vec2(std::fmod(v.x, m), std::fmod(v.y, m));
}

// 计算取余，返回一个由每个分量与给定向量取余得到的新向量
inline vec2 mod(crvec2 v, crvec2 m)
{
    return vec2(std::fmod(v.x, m.x), std::fmod(v.y, m.y));
}

// 计算绝对值，返回一个由每个分量的绝对值得到的新向量
inline vec2 abs(crvec2 v)
{
    return vec2(std::abs(v.x), std::abs(v.y));
}

inline real vv_angle(crvec2 v1, crvec2 v2)
{
    real x = dot(v1.normalized(), v2.normalized());
    if (std::isnan(x))
        return std::numeric_limits<real>::quiet_NaN();
    if (x > 1.0)
        x = 1.0;
    else if (x < -1.0)
        x = -1.0;
    real angle = std::acos(x);
    if (angle < 0)
        angle += 2 * PI;
    return v1.cross(v2) > 0 ? angle : -angle;
}
/**************************************************************************************************************\ 
*  _______ _            _____                     _ _             _         _____           _                  *  
* |__   __| |          / ____|                   | (_)           | |       / ____|         | |                 *  
*    | |  | |__   ___ | |     ___   ___  _ __ __| |_ _ __   __ _| |_ ___ | (___  _   _ ___| |_ ___ _ __ ___    *  
*    | |  | '_ \ / _ \| |    / _ \ / _ \| '__/ _` | | '_ \ / _` | __/ _ \ \___ \| | | / __| __/ _ \ '_ ` _ \   *  
*    | |  | | | |  __/| |___| (_) | (_) | | | (_| | | | | | (_| | ||  __/ ____) | |_| \__ \ ||  __/ | | | | |  *  
*    |_|  |_| |_|\___| \_____\___/ \___/|_|  \__,_|_|_| |_|\__,_|\__\___||_____/ \__, |___/\__\___|_| |_| |_|  *  
*                                                                                 __/ |                        *  
*                                                                                |___/                         *
**								[Coordinate System (Coordinate Frame)]										  **
*
*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
*   The Coordinate System class is specifically encapsulated to simplify coordinate transformations
*   and derive geometric algorithms, capable of solving various problems related to coordinate system
*   transformations. The coordinate system operations exhibit a Lie group-like structure.
*   The coordinate system consists of three components: C = M (position) + S (scaling) * R (rotation).
*
*  *  *  *  *  *  *  *  *  *  *  *  Detailed Explanation  *  *  *  *  *  *  *  *  *  *  *  *  *  *
*   Coordinate system transformation is divided into three steps:
*						projection (/), translation (^), and restoration (*).
*
*   The coordinate system itself is denoted as C. Transformations between coordinate systems
*   can be expressed as G = C2 / C1 - I, where G represents the geometric gradient.
*						oper(/)  =  C1 * C2^-1
*						oper(\)  =  C1^-1 * C2
*
*   Specifically:
*   Define a vector V in an intrinsic coordinate system (assuming a flat space where vectors can
*   move freely without change). When observing V in a curved coordinate system, V appears different
*   at different points. Therefore, the coordinate system is position-dependent.
*
*   Take vectors V1 and V2 at adjacent points (1) and (2) respectively,
*   corresponding to coordinate systems C1 and C2. Then:
*						V  = V1 * C1 = V2 * C2 =>
*						V2 = V1 * C1 / C2, let R12 = C1 / C2 =>
*						V2 = V1 * R12
*
*   Based on the dual-frame normalization theory proposed in this paper,
*   the geometric connection operator is:
*           			G_μ = (c(u+h_μ) - c(u))/h_μ
*   where c is the intrinsic frame field and C is the embedding frame field.
*
*   The coordinate system can be used to compute spatial curvature. In the u,v coordinate system,
*   the curvature tensor is:
*						R_uv = G_u·G_v - G_v·G_u - G_[u,v]
*   where:
*			 	G_u = (c(u+Δ,v) - c(u,v)) / Δ
*			 	G_v = (c(u,v+Δ) - c(u,v)) / Δ
*			 	G_[u,v] = connection operator for coordinate commutator [∂_u, ∂_v]
*
*   For holonomic coordinate systems (spherical, toroidal, etc.), coordinate basis vectors commute:
*           			[∂_u, ∂_v] = 0  ⇒  G_[u,v] = 0
*   Thus the formula simplifies to: R_uv = G_u·G_v - G_v·G_u
*
*   **Measurement Function for Curvature Extraction:**
*   
*   The measurement function bridges frame bundle curvature to Riemannian geometry:
*           			M_{ijkl} = √det(g) · ⟨X e_l, e_k⟩
*   where:
*      			X = [G_u, G_v]              (Lie bracket curvature operator)
*      			e_k, e_l                    (tangent basis vectors)
*      			det(g)                      (determinant of metric tensor)
*      			⟨·,·⟩                       (inner product in embedding space)
*
*   **Riemann Curvature Extraction:**
*           			R_{ijkl} = M_{ijkl} / √det(g)
*
*   **Gaussian Curvature Calculation (verified implementation):**
*           			K = R_{1212} / det(g)
* 
*
*   This approach provides O(n³) computational complexity for full curvature analysis,
*   significantly faster than traditional O(n⁶) methods.
*
*/

// #define	NON_UNIFORM_SCALE
// ************************************************************************************************
//  |/_
// UC     3d Rotation Coordinate System（Base Coordinate System）
// ************************************************************************************************
struct  ucoord3
{
	static const ucoord3 ONE;
	//union {
		//struct {
			// basis 基向量
			vec3 ux;
			vec3 uy;
			vec3 uz;
		//};
		//real m[9]; // 矩阵用法
	//};
	ucoord3()
	{
		ux = vec3::UX; uy = vec3::UY; uz = vec3::UZ;
	}
    ucoord3(const ucoord3& c)
	{
		ux = c.ux; uy = c.uy; uz = c.uz;
	}
    ucoord3(const vec3& _ux, const vec3& _uy, const vec3& _uz)
	{
		ux = _ux; uy = _uy; uz = _uz;
	}
    ucoord3(const vec3& _ux, const vec3& _uy)
	{
		ux = _ux; uy = _uy; uz = ux.cross(uy);
	}
    ucoord3(real ang, const vec3& ax)
	{
		quaternion q(ang, ax);
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}
    ucoord3(real pit, real yaw, real rol)
	{
		quaternion q(pit, yaw, rol);
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}
	ucoord3(const quaternion& q)
	{
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}

	// uy方向 推测ux,uz
	void fromquat(const quaternion& q)
	{
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}
	void fromuy(const vec3& _uy)
	{
		quat q; q.from_vectors(uy, _uy);
		fromquat(q);
	}
	// 引用四元数的欧拉角转化
	void frompyr(real pit, real yaw, real rol)
	{
		fromquat({ pit, yaw, rol });
	}
	void frompyr(const vec3& pyr)
	{
		fromquat(quaternion(pyr.x, pyr.y, pyr.z));
	}
	vec3 topyr() const
	{
		return Q().to_eulers();
	}
	// 坐标系的欧拉角转化
	vec3 toeulers() const
	{
		return coord2eulers();
	}
	// 旋转差
	void from_vecs_R(const vec3& v1, const vec3& v2)
	{
		vec3  v = v1.cross(v2);
		real c = v1.dot(v2);
		real k = 1.0 / (1.0 + c);
		
		ux = { v.x * v.x * k + c,      v.y * v.x * k - v.z,    v.z * v.x * k + v.y };
		uy = { v.x * v.y * k + v.z,    v.y * v.y * k + c,      v.z * v.y * k - v.x };
		uz = { v.x * v.z * k - v.y,    v.y * v.z * k + v.x,    v.z * v.z * k + c   };
	}
	// 轴，向量1，2
	void from_ax_vecs(const vec3& ax, const vec3& v1, const vec3& v2)
	{
		vec3 pv1 = v1.crossdot(ax);
		vec3 pv2 = v2.crossdot(ax);
		real ang = acos(pv1.dot(pv2));
		quaternion q; q.ang_axis(ang, ax);
		fromquat(q);
	}
	bool same_dirs(const ucoord3& c) const
	{
		return ux == c.ux && uy == c.uy && uz == c.uz;
	}
	bool operator == (const ucoord3& c) const
	{
		return same_dirs(c);
	}
	bool operator != (const ucoord3& c) const
	{
		return !same_dirs(c);
	}
	vec3 operator[] (int index) const
	{
		if(index == 0)
			return ux;
		else if (index == 1)
			return uy;
		else if (index == 2)
			return uz;

		return vec3::ZERO;
	}

	// 乘法：在坐标系下定义一个向量，或者向量向父空间还原
	friend vec3 operator * (const vec3& v, const ucoord3& c)
	{
		return c.ux * (v.x) + c.uy * (v.y) + c.uz * (v.z);
	}
	ucoord3 operator * (const ucoord3& c) const
	{// C_child * C_parent * ...
		ucoord3 rc;
		rc.ux = ux.x * c.ux + ux.y * c.uy + ux.z * c.uz;
		rc.uy = uy.x * c.ux + uy.y * c.uy + uy.z * c.uz;
		rc.uz = uz.x * c.ux + uz.y * c.uy + uz.z * c.uz;

		return rc;
	}
	friend quaternion operator * (const quaternion& q, const ucoord3& c)
	{
		return  q * c.toquat();
	}
	ucoord3 operator * (const quaternion& q) const
	{
		ucoord3 rc;
		rc.ux = q * ux;
		rc.uy = q * uy;
		rc.uz = q * uz;
		return rc;
	}
	friend void operator *= (vec3& v, const ucoord3& c)
	{
		v = v * c;
	}
	void operator *= (const ucoord3& c)
	{
		*this = (*this) * c;
	}
	void operator *= (const quaternion& q)
	{
		ux = q * ux;
		uy = q * uy;
		uz = q * uz;
	}
	// 除法：向量向坐标系投影（对于非正交坐标系，建议再扩展）
    friend vec3 operator/(const vec3& v, const ucoord3& c)
	{
		return vec3(v.dot(c.ux), v.dot(c.uy), v.dot(c.uz));
	}
    friend void operator/=(vec3& v, const ucoord3& c)
	{
		v = v / c;
	}
	// oper(/) = C1 * C2^-1
    ucoord3 operator/(const ucoord3& c) const
	{
		ucoord3 rc;
		rc.ux = vec3(ux.dot(c.ux), ux.dot(c.uy), ux.dot(c.uz));
		rc.uy = vec3(uy.dot(c.ux), uy.dot(c.uy), uy.dot(c.uz));
		rc.uz = vec3(uz.dot(c.ux), uz.dot(c.uy), uz.dot(c.uz));
		return rc;
	}
    void operator/=(const ucoord3& c)
	{
		*this = (*this) / c;
	}
	friend quaternion operator / (const quaternion& q, const ucoord3& c)
	{
		return q * c.toquat().conjcopy();
	}
	ucoord3 operator / (const quaternion& q) const
	{
		return (*this) * q.conjcopy();
	}
	void operator /= (const quaternion& q)
	{
		*this = (*this) / q;
	}
	// oper(\) = C1^-1 * C2
	ucoord3 operator % (const ucoord3& c) const
	{
		return (*this).reversed() * c;
	}
	// oper(^)
	// 相空间的乘法运算,Ce^(th*v)
	// 如C表示某向量A在两点间的旋转，
	// 融合向量0<v<1,c=C^v; v=0时c=ONE,v=1时c=C
	ucoord3 operator ^ (const vec3& v) const
	{
		ucoord3 c = *this;
		c.ux = vec3::lerp(vec3::UX, c.ux, v.x); c.ux.normalize();
		c.uy = vec3::lerp(vec3::UY, c.uy, v.y); c.uy.normalize();
		c.uz = vec3::lerp(vec3::UZ, c.uz, v.z); c.uz.normalize();

		return c;
	}
	void operator ^= (const vec3& v)
	{
		(*this) = (*this) ^ v;
	}
	ucoord3 operator ^ (real f) const
	{
		// 四元数法
		return ucoord3((*this).toquat() ^ f);
	}
	void operator ^= (real f)
	{
		(*this) = (*this) ^ f;
	}
	// 转置(坐标轴交换）
	void transpose()
	{
		vec3 _ux = vec3(ux.x, uy.x, uz.x);
		vec3 _uy = vec3(ux.y, uy.y, uz.y);
		vec3 _uz = vec3(ux.z, uy.z, uz.z);
		ux = _ux; uy = _uy; uz = _uz;
	}
	ucoord3 transposed()
	{
		ucoord3 c = (*this);
		c.ux = vec3(ux.x, uy.x, uz.x);
		c.uy = vec3(ux.y, uy.y, uz.y);
		c.uz = vec3(ux.z, uy.z, uz.z);
		return c;
	}
	// 倒置
	void reverse()
	{
		(*this) = ONE / (*this);
	}
	ucoord3 reversed() const
	{
		return ONE / (*this);
	}
	// 翻转
	void flipX()
	{
		ux = -ux;
	}
	void flipY()
	{
		uy = -uy;
	}
	void flipZ()
	{
		uz = -uz;
	}
	vec3 dir() const
	{
		return (ux + uy + uz).normalized();
	}
	
	// 本征向量（坐标系作为旋转变换时候的特征）
	vec3 eigenvec() const
	{
		return toquat().axis();
	}
	real dot(const vec3& v) const
	{
		return v.dot(ux) + v.dot(uy) + v.dot(uz);
	}
	real dot(const ucoord3& c) const
	{
		return c.ux.dot(ux) + c.uy.dot(uy) + c.uz.dot(uz);
	}
	// 由电磁场计算引出的叉乘
	ucoord3 cross(const ucoord3& c) const
	{
		return ucoord3(
			vec3::UX * (uy.dot(c.uz) - uz.dot(c.uy)),
			vec3::UY * (uz.dot(c.ux) - ux.dot(c.uz)),
			vec3::UZ * (ux.dot(c.uy) - uy.dot(c.ux))
		);
	}
	// v1 x v2 = v1 * (C x v2)
	ucoord3 cross(const vec3& v) const
	{
		return ucoord3(
			ux.cross(v),
			uy.cross(v),
			uz.cross(v)
		);
	}
	// 坐标系到欧拉角
	vec3 coord2eulers() const
	{
		real c_eps = 1e-5;

		const ucoord3& rm = *this;
		real sy = sqrt(rm.ux.x * rm.ux.x + rm.uy.x * rm.uy.x);
		bool singular = sy < c_eps;

		real x, y, z;
		if (!singular)
		{
			x = atan2(rm.uz.y, rm.uz.z);
			y = atan2(-rm.uz.x, sy);
			z = atan2(rm.uy.x, rm.ux.x);
		}
		else
		{
			x = atan2(-rm.uy.z, rm.uy.y);
			y = atan2(-rm.uz.x, sy);
			z = 0;
		}
		//PRINT("rx: " << x * 180 / PI << ", ry: " << y * 180 / PI << ", rz: " << z * 180 / PI);
		//PRINT("rx: " << x << ", ry: " << y  << ", rz: " << z);
		return vec3(x, y, z);
	}
	ucoord3 eulers2coord(const vec3& eulers)
	{
		real x = eulers.x;
		real y = eulers.y;
		real z = eulers.z;

		real cx = cos(x);
		real sx = sin(x);
		real cy = cos(y);
		real sy = sin(y);
		real cz = cos(z);
		real sz = sin(z);

		ucoord3 result;
		result.ux.x = cy * cz;
		result.ux.y = -cy * sz;
		result.ux.z = sy;

		result.uy.x = cx * sz + sx * sy * cz;
		result.uy.y = cx * cz - sx * sy * sz;
		result.uy.z = -sx * cy;

		result.uz.x = sx * sz - cx * sy * cz;
		result.uz.y = sx * cz + cx * sy * sz;
		result.uz.z = cx * cy;

		return result;
	}

	// 转化为四元数, 注意四元数的乘法顺序
	quaternion toquat() const
	{
		return quat(coord2eulers());
	}
	quaternion Q() const
	{
		return quat(coord2eulers());
	}
	void Q(const quaternion& q)
	{
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}
	void Q(real qw, real qx, real qy, real qz)
	{
		quaternion q(qw, qx, qy, qz);
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
	}

	// 梯度坐标系 = 梯度 X 切空间
	// 相当于一阶坐标系的导数
	// C2 = UG * C1
	static ucoord3 ugrad(const ucoord3& c1, const ucoord3& c2)
	{
		return c1.reversed() * c2;
	}
	static ucoord3 R(const ucoord3& c1, const ucoord3& c2)
	{
		return c1.reversed() * c2;
	}

	// 方便函数, 注意 angle(u,_u) != +/-PI
	void rot(real angle, const vec3& ax)
	{
		quaternion q(angle, ax);
		ux = q * ux;
		uy = q * uy;
		uz = q * uz;
	}
	void rot(const quaternion& q)
	{
		ux = q * ux;
		uy = q * uy;
		uz = q * uz;
	}
	void uxto(const vec3& _ux)
	{
		*this *= quat(ux, _ux);
	}
	void uyto(const vec3& _uy)
	{
		*this *= quat(uy, _uy);
	}
	void uzto(const vec3& _uz)
	{
		*this *= quat(uz, _uz);
	}
	ucoord3 uxtoed(const vec3& _ux) const
	{
		return (*this) * quat(ux, _ux);
	}
	ucoord3 uytoed(const vec3& _uy) const
	{
		return (*this) * quat(uy, _uy);
	}
	ucoord3 uztoed(const vec3& _uz) const
	{
		return (*this) * quat(uz, _uz);
	}

	void dump(const std::string& name = "") const
	{
		PRINT("----" << name << "---");
		PRINTVEC3(ux);
		PRINTVEC3(uy);
		PRINTVEC3(uz);
	}
};

inline const ucoord3 ucoord3::ONE = {};

// ******************************************************************
//  |/_
// VC     3d Rotation & Scaling Coordinate System
// ******************************************************************
struct  vcoord3 : ucoord3
{
	static const vcoord3 ONE;

	vec3 s = vec3::ONE;		// 缩放

	vcoord3() {}
	vcoord3(const real& _s) : s(_s, _s, _s) {}
	vcoord3(real x, real y, real z) : s(x, y, z) {}
	vcoord3(const ucoord3& c) : ucoord3(c){}
	vcoord3(const ucoord3& c, const vec3& _s) : ucoord3(c), s(_s){}
	vcoord3(const vec3& _ux, const vec3& _uy, const vec3& _uz, const vec3& _s) : ucoord3(_ux, _uy, _uz), s(_s){ }
	vcoord3(const vec3& _ux, const vec3& _uy, const vec3& _uz) : ucoord3(_ux, _uy, _uz){}
	vcoord3(const quaternion& q) : ucoord3(q){}
	vcoord3(const quaternion& q, const vec3& _s) : ucoord3(q), s(_s) {}
	vcoord3(const vec3& _s) : s(_s) {}

	vec3 VX() const { return ux * s.x; }
	vec3 VY() const { return uy * s.y; }
	vec3 VZ() const { return uz * s.z; }

	const ucoord3& base() const
	{
		return static_cast<const ucoord3&>(*this);
	}
	void base(const ucoord3& ucd)
	{
		ux = ucd.ux; uy = ucd.uy; uz = ucd.uz;
	}
	const ucoord3& R() const
	{
		return static_cast<const ucoord3&>(*this);
	}
	const ucoord3& UC() const
	{
		return static_cast<const ucoord3&>(*this);
	}
	void UC(const ucoord3& ucd)
	{
		ux = ucd.ux; uy = ucd.uy; uz = ucd.uz;
	}

	// 乘法：在坐标系下定义一个向量
	friend vec3 operator * (const vec3& p, const vcoord3& c)
	{
		return c.ux * (c.s.x * p.x) + c.uy * (c.s.y * p.y) + c.uz * (c.s.z * p.z);
	}
	friend void operator *= (vec3& p, const vcoord3& c)
	{
		p = p * c;
	}
	vcoord3 operator * (const vec3& v) const
	{
		return (*this) * vcoord3(vec3::UX * v.x, vec3::UY * v.y, vec3::UZ * v.z);
	}
	void operator *= (const vec3& v)
	{
		*this = (*this) * v;
	}
	friend real operator * (const real& s, const vcoord3& c)
	{
		return s * ((c.s.x + c.s.y + c.s.z) / 3.0);
	}
	vcoord3 operator * (real _s) const
	{
		vcoord3 c = *this;
		{// C*S 缩放乘法
			c.s.x *= _s; c.s.y *= _s; c.s.z *= _s;
		}
		return c;
	}
	void operator *= (real _s)
	{
		*this = (*this) * _s;
	}
	vcoord3 operator * (const vcoord3& c) const
	{// Cchild * Cparent * ...
		vcoord3 rc;
#ifdef	NON_UNIFORM_SCALE
		rc.ux = (ux.x * s.x) * (c.ux * c.s.x) + (ux.y * s.x) * (c.uy * c.s.y) + (ux.z * s.x) * (c.uz * c.s.z);
		rc.uy = (uy.x * s.y) * (c.ux * c.s.x) + (uy.y * s.y) * (c.uy * c.s.y) + (uy.z * s.y) * (c.uz * c.s.z);
		rc.uz = (uz.x * s.z) * (c.ux * c.s.x) + (uz.y * s.z) * (c.uy * c.s.y) + (uz.z * s.z) * (c.uz * c.s.z);
		rc.normalize();
#else
		rc = ucoord3::operator*(c);
		rc.s = s * c.s;
#endif
		return rc;
	}
	void operator *= (const vcoord3& c)
	{
		*this = (*this) * c;
	}
	vcoord3 operator * (const quaternion& q) const
	{
		vcoord3 rc = *this;
		rc.ux = q * ux;
		rc.uy = q * uy;
		rc.uz = q * uz;
		return rc;
	}
	void operator *= (const quaternion& q)
	{
		*this = (*this) * q;
	}
	
	// 除法：向量向坐标系投影（对于非正交坐标系，建议再扩展）
	friend vec3 operator / (const vec3& v, const vcoord3& c)
	{
		return vec3(v.dot(c.ux) / c.s.x, v.dot(c.uy) / c.s.y, v.dot(c.uz) / c.s.z);
	}
	friend void operator /= (vec3& p, const vcoord3& c)
	{
		p = p / c;
	}
	vcoord3 operator / (const vec3& v) const
	{
		return (*this) / vcoord3(vec3::UX * v.x, vec3::UY * v.y, vec3::UZ * v.z);
	}
	void operator /= (const vec3& v)
	{
		*this = (*this) / v;
	}

	vcoord3 operator / (real _s) const
	{// C/S 缩放除法
		vcoord3 c = *this;
		c.s /= _s;
		return c;
	}
	void operator /= (real _s)
	{
		*this = (*this) / _s;
	}
	// oper(/) = C1 * C2^-1
	vcoord3 operator / (const vcoord3& c) const
	{
		vcoord3 rc;
#ifdef	NON_UNIFORM_SCALE
		vec3 vx = VX();
		vec3 vy = VY();
		vec3 vz = VZ();

		vec3 cvx = c.ux.normalized() / c.s.x;
		vec3 cvy = c.uy.normalized() / c.s.y;
		vec3 cvz = c.uz.normalized() / c.s.z;

		rc.ux = vec3(vx.dot(cvx), vx.dot(cvy), vx.dot(cvz));
		rc.uy = vec3(vy.dot(cvx), vy.dot(cvy), vy.dot(cvz));
		rc.uz = vec3(vz.dot(cvx), vz.dot(cvy), vz.dot(cvz));

		// rc.normalize();
#else
		rc = ucoord3::operator/(c);
		rc.s = s / c.s;
#endif
		return rc;
	}
	void operator /= (const vcoord3& c)
	{
		*this = (*this) / c;
	}
	vcoord3 operator / (const quaternion& q) const
	{
		return (*this) * q.conjcopy();
	}
	void operator /= (const quaternion& q)
	{
		*this = (*this) / q;
	}

	// 归一化
	void normalize(bool bscl = true)
	{
		s.x *= ux.len(); if (!is_zero(s.x)) ux /= s.x;
		s.y *= uy.len(); if (!is_zero(s.y)) uy /= s.y;
		s.z *= uz.len(); if (!is_zero(s.z)) uz /= s.z;
		if (!bscl)
			s = vec3::ONE;
	}
	vcoord3 normcopy(bool bscl = true) const
	{
		vcoord3 c = *this;
		c.normalize(bscl);
		return c;
	}

	// 倒置
	void reverse()
	{
		(*this) = ONE / (*this);
	}
	vcoord3 reversed() const
	{
		return ONE / (*this);
	}

	// Cross Product 由电磁场计算引出的叉乘
	vcoord3 cross(const vcoord3& c) const
	{
		vec3 vx = VX();
		vec3 vy = VY();
		vec3 vz = VZ();

		vec3 cvx = c.VX();
		vec3 cvy = c.VY();
		vec3 cvz = c.VZ();

		return vcoord3(
			vec3::UX * (vy.dot(cvz) - vz.dot(cvy)),
			vec3::UY * (vz.dot(cvx) - vx.dot(cvz)),
			vec3::UZ * (vx.dot(cvy) - vy.dot(cvx))
		);
	}
	// v1 x v2 = v1 * (C x v2)
	vcoord3 cross(const vec3& v) const
	{
		return vcoord3(
			VX().cross(v),
			VY().cross(v),
			VZ().cross(v)
		);
	}

	// Dot Product 
	real dot(const vec3& v) const
	{
		return v.dot(ux) * s.x + v.dot(uy) * s.y + v.dot(uz) * s.z;
	}
	real dot(const vcoord3& c) const
	{
		return c.VX().dot(VX()) + c.VY().dot(VY()) + c.VZ().dot(VZ());
	}
	// Metric Vector
	vec3 metric() const
	{
		vec3 vx = VX();
		vec3 vy = VY(); 
		vec3 vz = VZ();
		return vec3(vx.dot(vx), vy.dot(vy), vz.dot(vz));
	}
	void dump(const std::string& name = "") const
	{
		PRINT("----" << name << "---");
		PRINTVEC3(ux);
		PRINTVEC3(uy);
		PRINTVEC3(uz);
		PRINTVEC3(s);
	}
};

inline const vcoord3 vcoord3::ONE	= { };


// ******************************************************************
//  |/_
// C     3d Coordinate System
// ******************************************************************
struct  coord3 : vcoord3
{
	static const coord3 ZERO;
	static const coord3 ONE;

	union {
		vec3 o = vec3::ZERO;			// 原点
		struct {
			real x, y, z;
		};
	};

	coord3() : o(0, 0, 0) {}
	explicit coord3(real _s) : vcoord3(_s) {}
	coord3(real x, real y, real z) : o(x, y, z) {}
	coord3(const coord3& other) : o(other.o), vcoord3(other.ux, other.uy, other.uz, other.s) {}

	coord3(const ucoord3& uc) : vcoord3(uc){}
	coord3(const vcoord3& vc) : vcoord3(vc) {}

	coord3(const vec3& _o) : o(_o) {}
	coord3(const vec3& _o, real _s) : vcoord3(_s), o(_o) {}
	coord3(const vec3& _o,  const vec3& _s,  const vec3& _ux, const vec3& _uy, const vec3& _uz) : vcoord3(_ux, _uy, _uz, _s), o(_o){}
	coord3(const vec3& _o,  const vec3& _ux, const vec3& _uy, const vec3& _uz) : vcoord3(_ux, _uy, _uz), o(_o){ }
	coord3(const vec3& _o,  const ucoord3& c) : vcoord3(c), o(_o){}
	coord3(const vec3& _o,  const vec3& _s,  const ucoord3& c) : vcoord3(c, _s), o(_o) {}

	coord3(const vec3& _ux, const vec3& _uy, const vec3& _uz) : vcoord3(_ux, _uy, _uz) {}
	coord3(const vec3& _ux, const vec3& _uy) : vcoord3(_ux, _uy, ux.cross(uy)) {}

	coord3(const ucoord3& c,const vec3& _s, const vec3& _o) : vcoord3(c, _s), o(_o){}
	coord3(const ucoord3& c,const vec3& _o) : vcoord3(c), o(_o) {}

	coord3(real ang, const vec3& ax) : vcoord3(quaternion(ang, ax)) {}
    coord3(const quaternion& q) : vcoord3(q) {}
    coord3(const vec3& p, const quaternion& q, const vec3& _s = vec3::ONE) : vcoord3(q, _s), o(p) {}

	coord3(real x, real y, real z, real qw, real qx, real qy, real qz) : vcoord3(quaternion(qw, qx, qy, qz), vec3::ONE), o(x, y, z) {}
	coord3(real x, real y, real z, real rx, real ry, real rz)
	{
		real ang2rad = PI / 180.0;
		quaternion q(rx * ang2rad, ry * ang2rad, rz * ang2rad);
		ux = q * vec3::UX;
		uy = q * vec3::UY;
		uz = q * vec3::UZ;
		o = vec3(x, y, z);
	}

	// ============================================================================
	// 静态构造函数：从不同表示形式创建坐标系
	// ============================================================================

	// 从基向量创建坐标系
	static coord3 from_axes(const vec3& ux, const vec3& uy, const vec3& uz) {
		return coord3(vec3::ZERO, vec3::ONE, ux, uy, uz);
	}

	// 从旋转角度和轴创建坐标系
	static coord3 from_angle(real angle, const vec3& axis) {
		quaternion q(angle, axis);
		return coord3(vec3::ZERO, q);
	}

	// 从欧拉角创建坐标系
	static coord3 from_eulers(const vec3& pyr) {
		return coord3(vec3::ZERO, quaternion(pyr.x, pyr.y, pyr.z));
	}

	// 创建Look-At坐标系：常用于相机和物体朝向
	// eye: 观察点位置, target: 目标点, up: 上方向
	static coord3 look_at(const vec3& eye, const vec3& target, const vec3& up = vec3::UY) {
		vec3 zaxis = (target - eye).normalized();  // 前方向
		vec3 xaxis = up.cross(zaxis).normalized(); // 右方向
		vec3 yaxis = zaxis.cross(xaxis);           // 上方向
		return coord3(eye, xaxis, yaxis, zaxis);
	}

	// 从位置和朝向向量创建坐标系
	static coord3 from_forward(const vec3& pos, const vec3& forward, const vec3& up = vec3::UY) {
		vec3 zaxis = forward.normalized();
		vec3 xaxis = up.cross(zaxis).normalized();
		vec3 yaxis = zaxis.cross(xaxis);
		return coord3(pos, xaxis, yaxis, zaxis);
	}

	operator quaternion() const
	{
		return toquat();
	}
    operator vec3() const
	{
		return o;
	}

    vec3 VX()	const { return ux * s.x; }
	vec3 VY()	const { return uy * s.y; }
	vec3 VZ()	const { return uz * s.z; }

	void VX(const vec3& vx)	{ real r = vx.len(); ux = vx / r; s.x = r; }
	void VY(const vec3& vy)	{ real r = vy.len(); uy = vy / r; s.y = r; }
	void VZ(const vec3& vz)	{ real r = vz.len(); uz = vz / r; s.z = r; }

	vec3 X()	const { return ux * s.x + vec3::UX * o.x; }
	vec3 Y()	const { return uy * s.y + vec3::UY * o.y; }
	vec3 Z()	const { return uz * s.z + vec3::UZ * o.z; }

	// 旋转坐标系
    const ucoord3& ucoord() const
	{
		return static_cast<const ucoord3&>(*this);
	}
    void ucoord(const ucoord3& ucd)
	{
		ux = ucd.ux; uy = ucd.uy; uz = ucd.uz;
	}
    void ucoord(vec3 _ux, vec3 _uy, vec3 _uz)
	{
		ux = _ux; uy = _uy; uz = _uz;
	}
	const ucoord3& R() const
	{
		return static_cast<const ucoord3&>(*this);
	}
    const ucoord3& UC() const
	{
		return static_cast<const ucoord3&>(*this);
	}
    void UC(const ucoord3& ucd)
	{
		ux = ucd.ux; uy = ucd.uy; uz = ucd.uz;
	}
    void UC(vec3 _ux, vec3 _uy, vec3 _uz)
	{
		ux = _ux; uy = _uy; uz = _uz;
	}
	// 向量坐标系 = 方向 X 缩放
    const vcoord3& vcoord() const
	{
		return static_cast<const vcoord3&>(*this);
	}
    const vcoord3& VC() const
	{
		return static_cast<const vcoord3&>(*this);
	}
	// 姿态
    coord3 pose()
	{
		return { ucoord(), vec3::ONE, o };
	}
	// 位置
    vec3 pos() const
	{
		return o;
	}
	// 向量
    vec3 tovec() const
	{
		return ux * s.x + uy * s.y + uz * s.z;
	}
    coord3 operator=(const coord3& c)
	{
		o = c.o;
		s = c.s;
		ux = c.ux; uy = c.uy; uz = c.uz;
		return (*this);
	}
    bool equal_dirs(const coord3& c) const
	{
		return ux == c.ux && uy == c.uy && uz == c.uz;
	}
    bool operator==(const coord3& c) const
	{
		return o == c.o && s == c.s && equal_dirs(c);
	}
    bool operator!=(const coord3& c) const
	{
		return o != c.o || s != c.s || !equal_dirs(c);
	}
	// +/- 运算
    coord3 operator+(const coord3& c) const
	{
		coord3 rc;
		rc.ux = VX() + c.VX();
		rc.uy = VY() + c.VY();
		rc.uz = VZ() + c.VZ();

		rc.s = vec3::ONE;
		rc.o = o + c.o;
		return rc;
	}
    coord3 operator+=(const coord3& c)
	{
		*this = (*this) + c;
		return *this;
	}
    coord3 operator+(const vec3& v) const
	{
		coord3 c = (*this); c.o += v;
		return c;
	}
    coord3 operator+=(const vec3& v)
	{
		*this = *this + v;
		return *this;
	}
    friend vec3 operator+(const vec3& p, const coord3& c)
	{
		return p + c.o;
	}
    friend void operator+=(vec3& p, const coord3& c)
	{
		p = p + c;
	}
    friend vec3 operator-(const vec3& p, const coord3& c)
	{
		return p - c.o;
	}
    friend void operator-=(vec3& p, const coord3& c)
	{
		p = p - c;
	}
    coord3 operator-(const coord3& c) const
	{
		coord3 rc;
		rc.ux = VX() - c.VX();
		rc.uy = VY() - c.VY();
		rc.uz = VZ() - c.VZ();
		
		rc.s = vec3::ONE;
		rc.o = o - c.o;
		return rc;
	}
	coord3 operator-() const
	{
		coord3 c = (*this);
		c.o = -c.o;
		return c;
	}
    coord3 operator-(const vec3& v) const
	{
		coord3 c = (*this); c.o -= v;
		return c;
	}
    coord3 operator-=(const vec3& v)
	{
		*this = *this - v;
		return *this;
	}

	// 乘法：在坐标系下定义一个向量
    friend vec3 operator*(const vec3& p, const coord3& c)
	{
		return c.ux * (c.s.x * p.x) + c.uy * (c.s.y * p.y) + c.uz * (c.s.z * p.z) + c.o;
	}
    friend void operator*=(vec3& p, const coord3& c)
	{
		p = p * c;
	}
    coord3 operator*(const vec3& v) const
	{
		return (*this) * coord3(vec3::UX * v.x, vec3::UY * v.y, vec3::UZ * v.z);
	}
    void operator*=(const vec3& v)
	{
		*this = (*this) * v;
	}
    coord3 operator*(real _s) const
	{
		coord3 c = *this;
		{// C*S 缩放乘法
			c.s *= _s;
			c.o *= _s;
		}
		return c;
	}
    void operator*=(real _s)
	{
		*this = (*this) * _s;
	}
    coord3 operator*(const coord3& c) const
	{// Cchild * Cparent * ...
		coord3 rc = vcoord3::operator*(c);
		rc.o = c.o + (o.x * c.s.x) * c.ux + (o.y * c.s.y) * c.uy + (o.z * c.s.z) * c.uz;
		return rc;
	}
    coord3 operator*=(const coord3& c)
	{
		*this = (*this) * c;
		return *this;
	}
	coord3 operator*(const vcoord3& c) const
	{// Cchild * Cparent * ...
		coord3 rc = vcoord3::operator*(c);
		rc.o = (o.x * c.s.x) * c.ux + (o.y * c.s.y) * c.uy + (o.z * c.s.z) * c.uz;
		return rc;
	}
	coord3 operator*=(const vcoord3& c)
	{
		*this = (*this) * c;
		return *this;
	}
	coord3 operator*(const ucoord3& c) const
	{// Cchild * Cparent * ...
		coord3 rc = ucoord3::operator*(c);
		rc.o = (o.x) * c.ux + (o.y) * c.uy + (o.z) * c.uz;
		return rc;
	}
	coord3 operator*=(const ucoord3& c)
	{
		*this = (*this) * c;
		return *this;
	}
    coord3 operator*(const quaternion& q) const
	{
		coord3 rc = *this;
		rc.ux = q * ux;
		rc.uy = q * uy;
		rc.uz = q * uz;
		rc.o = q * rc.o;
		return rc;
	}
    coord3 operator*=(const quaternion& q)
	{
		*this = (*this) * q;
		return *this;
	}

	// 除法：向量向坐标系投影（对于非正交坐标系，建议再扩展）
    friend vec3 operator/(const vec3& p, const coord3& c)
	{
		vec3 v = p - c.o;
		v = v / c.s;
		return vec3(v.dot(c.ux), v.dot(c.uy), v.dot(c.uz));
	}
    friend void operator/=(vec3& p, const coord3& c)
	{
		p = p / c;
	}
    coord3 operator/(const vec3& v) const
	{
		return (*this) / coord3(vec3::UX * v.x, vec3::UY * v.y, vec3::UZ * v.z);
	}
    void operator/=(const vec3& v)
	{
		*this = (*this) / v;
	}
	friend real operator/(real _s, const coord3& c)
	{
		return _s / c.s.mean();
	}
	coord3 operator/(real _s) const
	{// C/S 缩放除法
		coord3 c = *this;
		c.s /= _s;
		c.o /= _s;
		return c;
	}
    void operator/=(real _s)
	{
		*this = (*this) / _s;
	}
	// oper(/) = C1 * C2^ - 1
    coord3 operator/(const coord3& c) const
	{
		coord3 rc = vcoord3::operator/(c);
		rc.o = o - c.o;
		rc.o = vec3(rc.o.dot(c.ux) / c.s.x, rc.o.dot(c.uy) / c.s.y, rc.o.dot(c.uz) / c.s.z);
		return rc;
	}
    coord3 operator/=(const coord3& c)
	{
		*this = (*this) / c;
		return *this;
	}
	coord3 operator/(const vcoord3& c) const
	{
		coord3 rc = vcoord3::operator/(c);
		rc.o = o;
		rc.o = vec3(rc.o.dot(c.ux) / c.s.x, rc.o.dot(c.uy) / c.s.y, rc.o.dot(c.uz) / c.s.z);
		return rc;
	}
	coord3 operator/=(const vcoord3& c)
	{
		*this = (*this) / c;
		return *this;
	}
	coord3 operator/(const ucoord3& c) const
	{
		coord3 rc = ucoord3::operator/(c);
		rc.o = o;
		rc.o = vec3(rc.o.dot(c.ux), rc.o.dot(c.uy), rc.o.dot(c.uz));
		return rc;
	}
	coord3 operator/=(const ucoord3& c)
	{
		*this = (*this) / c;
		return *this;
	}
    coord3 operator/(const quaternion& q) const
	{
		return (*this) * q.conjcopy();
	}
    void operator/=(const quaternion& q)
	{
		*this = (*this) / q;
	}
	// oper(\) = C1^-1 * C2
    coord3 operator%(const coord3& c) const
	{
		return (*this).reversed() * c;
	}
	// 倒置
	void reverse()
	{
		(*this) = ONE / (*this);
	}
	coord3 reversed() const
	{
		return ONE / (*this);
	}
	// 由李符号引出的叉乘，更加符合群论
	coord3 lie_cross(const coord3& c) const
	{
		return (*this) * c - c * (*this);
	}

	// ============================================================================
	// 几何运算：插值、距离等
	// ============================================================================
	
	// 线性插值：位置和旋转的独立插值
	static coord3 lerp(const coord3& c1, const coord3& c2, real t)
	{
		coord3 result;
		result.o = vec3::lerp(c1.o, c2.o, t);           // 位置线性插值
		result.s = vec3::lerp(c1.s, c2.s, t);           // 缩放线性插值
		result.Q(quaternion::slerp(c1.Q(), c2.Q(), t)); // 旋转球面插值
		return result;
	}

	// 球面线性插值：使用四元数进行平滑旋转插值
	static coord3 slerp(const coord3& c1, const coord3& c2, real t)
	{
		coord3 result;
		result.o = vec3::lerp(c1.o, c2.o, t);
		result.s = vec3::lerp(c1.s, c2.s, t);
		result.Q(quaternion::slerp(c1.Q(), c2.Q(), t));
		return result;
	}

	// 计算两个坐标系间的距离（位置差）
	real distance_to(const coord3& other) const
	{
		return (o - other.o).len();
	}

	// 计算两个坐标系间的旋转角度差
	real rotation_distance_to(const coord3& other) const
	{
		return Q().angle_to(other.Q());
	}

	// ============================================================================
	// 曲率计算
	// ============================================================================
	// 梯度坐标系
	// V2 - V1 = V1 * G, 其中 G = C2 / C1 - I
	static coord3 grad(const coord3& c1, const coord3& c2)
	{
		return c2 / c1 - ONE;
	}
	
	vec3 metric() const
	{
		// 对于曲面，我们通常只关心 u,v 方向的切向量
		vec3 vx = VX();  // ∂r/∂u 方向
		vec3 vy = VY();  // ∂r/∂v 方向

		real E = vx.dot(vx);  // g_uu = ∂r/∂u · ∂r/∂u
		real F = vx.dot(vy);  // g_uv = ∂r/∂u · ∂r/∂v  
		real G = vy.dot(vy);  // g_vv = ∂r/∂v · ∂r/∂v

		return vec3(E, F, G);
	}
	// 计算第一基本形式的行列式
	real metric_det() const 
	{
		vec3 vx = VX();
		vec3 vy = VY();
		vec3 vz = VZ();  // 这个vz不应该参与2D曲面计算！

		real E = vx.dot(vx);
		real F = vx.dot(vy);
		real G = vy.dot(vy);

		return E * G - F * F;
	}

	static coord3 lie_bracket(const coord3& A, const coord3& B) {
		// [A, B] = A * B - B * A
		return A * B - B * A;  // 需要正确定义这个运算
	}
	
	std::string serialise() const
	{
		vec3 eu = coord2eulers();
		return o.serialise() + "," + eu.serialise();
	}
	void dump(const std::string& name = "") const
	{
		PRINT("|/_ : " << name);
		PRINTVEC3(o);
		PRINTVEC3(s);
		PRINTVEC3(ux);
		PRINTVEC3(uy);
		PRINTVEC3(uz);		
	}
	
};

inline const coord3 coord3::ZERO = {ucoord3::ONE, vec3::ZERO, vec3::ZERO };
inline const coord3 coord3::ONE = {};

// ==============================================================================
// 扩展定义 - 添加缺失的方法包装函数
// ==============================================================================

// ==============================================================================
// vector3 扩展方法
// ==============================================================================
// norm - in-place归一化 (作为包装函数)
inline vector3& vec3_norm(vector3& v) {
    real len = v.len();
    if (len > EPSILON) {
        v.x /= len;
        v.y /= len;
        v.z /= len;
    }
    return v;
}

// reflect - 反射
inline vector3 vec3_reflect(const vector3& v, const vector3& normal) {
    return v - normal * 2.0 * v.dot(normal);
}

// distance - 距离
inline real vec3_distance(const vector3& v1, const vector3& v2) {
    return (v2 - v1).len();
}

// ==============================================================================
// vector2 扩展方法
// ==============================================================================
inline vector2& vec2_norm(vector2& v) {
    real len = v.len();
    if (len > EPSILON) {
        v.x /= len;
        v.y /= len;
    }
    return v;
}

inline real vec2_distance(const vector2& v1, const vector2& v2) {
    return (v2 - v1).len();
}

inline vector2 vec2_lerp(const vector2& v1, const vector2& v2, real t) {
    return v1 * (1.0 - t) + v2 * t;
}

// ==============================================================================
// quaternion 扩展方法
// ==============================================================================
// norm - in-place归一化
inline quaternion& quat_norm(quaternion& q) {
    real len = sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
    if (len > EPSILON) {
        q.w /= len;
        q.x /= len;
        q.y /= len;
        q.z /= len;
    }
    return q;
}

// normcopy - 返回归一化副本
inline quaternion quat_normcopy(const quaternion& q) {
    quaternion result = q;
    return quat_norm(result);
}

// rotate - 用四元数旋转向量
inline vector3 quat_rotate(const quaternion& q, const vector3& v) {
    // q * v * q^-1
    quaternion qv(0, v.x, v.y, v.z);
    quaternion q_inv(q.w, -q.x, -q.y, -q.z);  // 单位四元数的逆
    quaternion result = q * qv * q_inv;
    return vector3(result.x, result.y, result.z);
}

// ==============================================================================
// coord3 扩展方法
// ==============================================================================
// to_world - 局部坐标转世界坐标
inline vector3 coord3_to_world(const coord3& c, const vector3& local_point) {
    return c.o + c.ux * local_point.x + c.uy * local_point.y + c.uz * local_point.z;
}

// to_local - 世界坐标转局部坐标
inline vector3 coord3_to_local(const coord3& c, const vector3& world_point) {
    vector3 diff = world_point - c.o;
    return vector3(diff.dot(c.ux), diff.dot(c.uy), diff.dot(c.uz));
}

// ==============================================================================
// 插值函数 - blend系列 (添加缺失的重载)
// ==============================================================================
// real 版本已经存在，添加 vector2, vector3, quaternion, coord3 版本

inline vector2 blend(const vector2& v1, const vector2& v2, real alpha, real power = 1.0) {
    alpha = clamp(alpha, 0.0, 1.0);
    if (power != 1.0)
        alpha = pow(alpha, power);
    return v1 * (1.0 - alpha) + v2 * alpha;
}

inline vector3 blend(const vector3& v1, const vector3& v2, real alpha, real power = 1.0) {
    alpha = clamp(alpha, 0.0, 1.0);
    if (power != 1.0)
        alpha = pow(alpha, power);
    return v1 * (1.0 - alpha) + v2 * alpha;
}

inline quaternion blend(const quaternion& q1, const quaternion& q2, real alpha, real power = 1.0) {
    alpha = clamp(alpha, 0.0, 1.0);
    if (power != 1.0)
        alpha = pow(alpha, power);
    return quaternion::slerp(q1, q2, alpha);
}

inline coord3 blend(const coord3& c1, const coord3& c2, real alpha, real power = 1.0) {
    alpha = clamp(alpha, 0.0, 1.0);
    if (power != 1.0)
        alpha = pow(alpha, power);

    vector3 pos = blend(c1.o, c2.o, alpha, 1.0);
    quaternion q1 = c1.Q();
    quaternion q2 = c2.Q();
    quaternion q = blend(q1, q2, alpha, 1.0);
    vector3 scale = blend(c1.s, c2.s, alpha, 1.0);

    return coord3(pos, q, scale);
}

// ==============================================================================
// slerp 系列 (球面线性插值) - blender命名空间
// ==============================================================================
namespace blender {
    inline vector3 slerp(const vector3& v1, const vector3& v2, real t) {
        real dot = v1.dot(v2);
        dot = clamp(dot, -1.0, 1.0);

        real theta = acos(dot) * t;
        vector3 relative = (v2 - v1 * dot).normcopy();

        return v1 * cos(theta) + relative * sin(theta);
    }

    inline quaternion slerp(const quaternion& q1, const quaternion& q2, real t) {
        return quaternion::slerp(q1, q2, t);
    }

    inline coord3 slerp(const coord3& c1, const coord3& c2, real t) {
        vector3 pos = c1.o * (1.0 - t) + c2.o * t;
        quaternion q = quaternion::slerp(c1.Q(), c2.Q(), t);
        vector3 scale = c1.s * (1.0 - t) + c2.s * t;
        return coord3(pos, q, scale);
    }

    // lerpPQ - 位置线性插值 + 旋转球面插值
    inline coord3 lerpPQ(const coord3& c1, const coord3& c2, real t) {
        vector3 pos = c1.o * (1.0 - t) + c2.o * t;  // 位置线性插值
        quaternion q = quaternion::slerp(c1.Q(), c2.Q(), t);  // 旋转球面插值
        vector3 scale = c1.s * (1.0 - t) + c2.s * t;
        return coord3(pos, q, scale);
    }
}

// 导出到全局命名空间
using blender::slerp;
using blender::lerpPQ;

#endif // PMSYS_MINIMAL_HPP