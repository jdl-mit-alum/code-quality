///////////////////////////////////////////////////////////////////////////////
/// @file goto_test.h.cpp
/// Copyright(c) 2008-2016 Jonathan D. Lettvin, All Rights Reserved
/// @author Jonathan D. Lettvin
/// @date 20080505
/// @brief read numerical text data with optimization and error-handling.
///        Implement mathematically provable perfect implementations of
///        high-speed data lexers for all possible text lexemes.
///        Test edge-cases with built-in unit tests.
/// Updated 20160515 to remove new warnings and clarify Alternates.
/// This code assumes 8-bit bytes.
///////////////////////////////////////////////////////////////////////////////
///   COMPILATION: (Express built-in unit-tests)
/// g++ -Wall -DLETTVIN_LEXERS_H_CPP_UNIT -o goto_test goto_test.h.cpp
///////////////////////////////////////////////////////////////////////////////
///   EXAMPLE USAGE: (fixed specified width lexer)
///
/// char source[ ] = "1234";
/// char *s = source;
/// unsigned long long error, target;
///
/// target = Lettvin::lexDecU64_Instance( s, target, error, digits );
/// target = Lettvin::lexDecU64_Instance( s, target, error, digits, hi );
/// target = Lettvin::lexDecU64_Instance( s, target, error, digits, hi, lo );
///
/// where digits is the number of digits to process.
/// where hi and lo are the highest and lowest permitted value.
/// where s changes to point into source immediately following non-error input.
/// where error is a flag indicating error.
/// If error is already set, no lexing is done.
/// If lexed number falls outside hi lo range, s is unchanged.
/// See UnitTest examples below for edge case analysis.
///////////////////////////////////////////////////////////////////////////////
///   METHODS:
/// Pass/return reference prevents data copying and stack construction cost.
/// Jump table eliminates typical switch case cost.
/// JIT (Just-In-Time) jump table filling for first-time cost only.
/// Jcond use designed to have 0 clock cost due to locality and UV pipes.
/// Prefilled data tables enabling column summing with minimum cost.
///////////////////////////////////////////////////////////////////////////////
///   RESTRICTIONS:
/// Jump table implementation is dependent on g++ syntax/semantics.
///////////////////////////////////////////////////////////////////////////////
///   IMPLEMENTED:
/// lexDecU64t: decimal representation into unsigned long long
///////////////////////////////////////////////////////////////////////////////
/// @mainpage Unsigned long long high performance lexer using computed goto.
///////////////////////////////////////////////////////////////////////////////
#if 0
/* EXPECTED OUTPUT:
///////////////////////////////////////////////////////////////////////////////
goto_test.h.cpp May  8 2008 10:41:59 UNIT TEST: starts Alternate style
Lettvin::u08t  1 ==  1
Lettvin::s08t  1 ==  1
Lettvin::u16t  2 ==  2
Lettvin::s16t  2 ==  2
Lettvin::u32t  4 ==  4
Lettvin::s32t  4 ==  4
Lettvin::f32t  4 ==  4
Lettvin::u64t  8 ==  8
Lettvin::s64t  8 ==  8
Lettvin::f64t  8 ==  8
                   IN                  BAD                  OUT  N E
                    0                               42951965936  1 0
                    1                                         1  1 0
                    2                                         2  1 0
                   10                                        10  2 0
                  900                                       900  3 0
                 8000                                      8000  4 0
                70000                                     70000  5 0
               600000                                    600000  6 0
              5000000                                   5000000  7 0
             40000000                                  40000000  8 0
            300000000                                 300000000  9 0
           2000000000                                2000000000 10 0
          10000000000                               10000000000 11 0
         900000000000                              900000000000 12 0
        8000000000000                             8000000000000 13 0
       70000000000000                            70000000000000 14 0
      600000000000000                           600000000000000 15 0
     5000000000000000                          5000000000000000 16 0
    40000000000000000                         40000000000000000 17 0
   300000000000000000                        300000000000000000 18 0
  2000000000000000000                       2000000000000000000 19 0
 10000000000000000000                      10000000000000000000 20 0
 18446744073709551615                      18446744073709551615 20 0
 18446744073709551616 18446744073709551616                    0  0 1
 20000000000000000000 20000000000000000000                    0  0 1
Illegal request for digit count > 20
Illegal request for digit count == 0
                    2                    2                    0  0 1
 18446744073709551615                      18446744073709551615 20 0
                    0                                         0  1 0
 18446744073709551615                      18446744073709551615 20 0
                    0                                         0  1 0
 18446744073709551615                      18446744073709551615 20 0
                    0                                         0  1 0
lexers.h.cpp May  8 2008 10:41:59 UNIT TEST: ends Alternate style
///////////////////////////////////////////////////////////////////////////////
*/
#endif

#define Alternate 0  ///< Identical logic, different appearance.

#ifndef LETTVIN_LEXERS_H_CPP
#define LETTVIN_LEXERS_H_CPP

#include <iostream>
#include <sstream>
#include <string>
#include <iomanip>
#include <exception>
#include <cstring>

namespace Lettvin {

#ifndef LETTVIN_TYPES
#define LETTVIN_TYPES
    /// @brief Types to support coding conventions/simplified param passing.
    ///        The regularity of the naming convention aids in quick analysis.
    ///        These types should be moved to a file.  Perhaps LettvinTypes.h
    ///        u =  unsigned
    ///        s =    signed
    ///       08 =    8 bits
    ///       16 =   16 bits
    ///       32 =   32 bits
    ///       64 =   64 bits
    ///       96 =   96 bits
    ///      128 =  128 bits
    ///        f =     float
    ///        t =      type
    ///        p =   pointer
    ///        r = reference
    typedef unsigned long long  u64t, *u64p, &u64r, *&u64pr;  // NOLINT
    typedef unsigned       int  u32t, *u32p, &u32r, *&u32pr;
    typedef unsigned     short  u16t, *u16p, &u16r, *&u16pr;  // NOLINT
    typedef unsigned      char  u08t, *u08p, &u08r, *&u08pr;

    typedef          long long  s64t, *s64p, &s64r, *&s64pr;  // NOLINT
    typedef                int  s32t, *s32p, &s32r, *&s32pr;
    typedef              short  s16t, *s16p, &s16r, *&s16pr;  // NOLINT
    typedef               char  s08t, *s08p, &s08r, *&s08pr;

    /// On AMD64 long double is 128.  On WIN32 it is 96
    // typedef        long double  f96t, *f96p, &f96r, *&f96pr;  //96 or 128
    // typedef        long double f128t,*f128p,&f128r,*&f128pr;  //96 or 128
    typedef             double  f64t, *f64p, &f64r, *&f64pr;
    typedef              float  f32t, *f32p, &f32r, *&f32pr;

    /// Until the long double size issue is addressed, 10 lexers must be made.
    /// One each: u08t, s08t, u16t, s16t, u32t, s32t, u64t, s64t, f32t, f64t.
    /// After addressing long doubles, one lexer for each size will be made
    /// for each useful representation such as decimal, base36.
    /// Other representations such as binary, octal, hexadecimal are ignored
    /// since use in financial data hasn't yet been established in FE-DEV.

    /// Examine sample output above to observe what this pair of macros do.
    /// CONFIRM_DATA_SIZE  enforces that data types have the specified size.
    /// CONFIRM_DATA_SIZES performs enforcement over all relevant data types.
    /// Note the u0 and s0 in the first two instances of CONFIRM_DATA_SIZE.
    /// These compensates for OCTAL numbers beginning with 0 such that
    /// a compiler sees the number 08 as a lexical error.
    /// Also note the t argument is required to append the 't' to each type.
#define CONFIRM_DATA_SIZE(b, w, t) \
    std::cout << \
    "Lettvin::" #b #w #t << " " << \
    std::setw(2) << sizeof(Lettvin::b##w##t) << \
    " == " << \
    std::setw(2) << (w/8) << \
    std::endl; \
    if (sizeof(Lettvin::b##w##t) != (w/8)) \
    throw("Size expectation violated.");
#define CONFIRM_DATA_SIZES \
    CONFIRM_DATA_SIZE(u0, 8, t) \
    CONFIRM_DATA_SIZE(s0, 8, t) \
    CONFIRM_DATA_SIZE(u, 16, t) \
    CONFIRM_DATA_SIZE(s, 16, t) \
    CONFIRM_DATA_SIZE(u, 32, t) \
    CONFIRM_DATA_SIZE(s, 32, t) \
    CONFIRM_DATA_SIZE(f, 32, t) \
    CONFIRM_DATA_SIZE(u, 64, t) \
    CONFIRM_DATA_SIZE(s, 64, t) \
    CONFIRM_DATA_SIZE(f, 64, t)
    /// CONFIRM_DATA_SIZE(f, 96, t)
    /// CONFIRM_DATA_SIZE(f, 128, t)

#endif  // LETTVIN_TYPES

class lexDecU64t {
 public:
            inline u64t &
                operator()(
                        u64r ull,
                        s08pr s,
                        u64t &e,                      // NOLINT
                        const size_t &d = 20,
                        u64t r = top,
                        u64t b = zip
                        ) {
#ifndef __GNUC__
#else
                    static void *DIGITS[256];   /// column-count jump table
                    s08p o = s;

                    /// Do not perform this function
                    /// if a prior error has been detected.
                    if ((e |= (d > 20))) goto err;
                    if (!DIGITS[0]) goto fill;
                    ull = zip;
                    u64t t;    /// temporary column value
                    // std::cout << std::endl << s << ":" << *s << std::endl;

run:    goto *(DIGITS[d]);
        ///********************************************************************
        /// Failure is slightly more expensive than success, as it should be.
        /// since the JC, JNC family consume 0 clocks if branch is not taken.
        /// This is a property of Intel iAPX86 prefetch queues and UV pipes.
        /// So, once the initialization takes place, this is 0 cost.
        /// Calculate number for the precise number of digits requested.
        /// This table of addresses permits inexpensive bypassing of
        /// unnecessary branchings and calculations.
        /// Idea: accumulate digits in each x10 column of the target number.
        /// Breakdown of operations in the next 20 lines:
        /// s is a pointer to the current character to lex.
        /// *s fetches that character.
        /// col[ 17 ][ *s ] indexes into the 17th table of 256 u64t values.
        ///********************************************************************
        /// HOW TO READ THESE LINES:
        /// If not error
        /// Check to see if this digit is forbidden in this column
        ///   Any digit other than 0 or 1 in column index 19 is forbidden.
        ///   This is because 0xFFFFFFFFFFFFFFFFULL == 18446744073709551615
        ///   so the most significant digit must never be greater than 1.
        ///   It is also because a non-digit should cause an error.
        /// If not, check to see if digit would overflow the remainder
        /// If not, reduce remainder, add digit in column and advance pointer.
        ///********************************************************************
#if Alternate
#define DECU64COLUMN(n) \
        c##n: \
        e || \
        (e|=inv[n][static_cast<int>(*s)]) || \
        (e|=((t=col[n][static_cast<int>(*s)]) > r)) || \
        ((r-=t), (ull+=t), (++s))
        DECU64COLUMN(19);
        DECU64COLUMN(18);
        DECU64COLUMN(17);
        DECU64COLUMN(16);
        DECU64COLUMN(15);
        DECU64COLUMN(14);
        DECU64COLUMN(13);
        DECU64COLUMN(12);
        DECU64COLUMN(11);
        DECU64COLUMN(10);
        DECU64COLUMN(9);
        DECU64COLUMN(8);
        DECU64COLUMN(7);
        DECU64COLUMN(6);
        DECU64COLUMN(5);
        DECU64COLUMN(4);
        DECU64COLUMN(3);
        DECU64COLUMN(2);
        DECU64COLUMN(1);
        DECU64COLUMN(0);
#else
#define DECU64COLPN(p, n) c##p##n: \
        e || \
        (e|=inv[n][static_cast<int>(*s)]) || \
        (e|=((t=col[n][static_cast<int>(*s)]) > r)) || \
        ((r-=t), (ull+=t), (++s))

        DECU64COLPN(1, 9);
        DECU64COLPN(1, 8);
        DECU64COLPN(1, 7);
        DECU64COLPN(1, 6);
        DECU64COLPN(1, 5);
        DECU64COLPN(1, 4);
        DECU64COLPN(1, 3);
        DECU64COLPN(1, 2);
        DECU64COLPN(1, 1);
        DECU64COLPN(1, 0);
        DECU64COLPN(0, 9);
        DECU64COLPN(0, 8);
        DECU64COLPN(0, 7);
        DECU64COLPN(0, 6);
        DECU64COLPN(0, 5);
        DECU64COLPN(0, 4);
        DECU64COLPN(0, 3);
        DECU64COLPN(0, 2);
        DECU64COLPN(0, 1);
        DECU64COLPN(0, 0);
#endif
        e |= (ull < b);       ///< See if value fell below minimum
        if (!e) return ull;    ///< This return bypasses any further execution
err:    s = o;              ///< On failure, restore the pointer
        return ull = zip;       ///< This return took extra instructions
fill:
        /// For the cost of expanding 20 instructions
        /// the initialization of the inlined jump table is available
        /// to be performed by every potential client for its own table.
        /// In the style of JIT compilation, this is performed
        /// the first time through any client call of this code.
        for (size_t i = 0; i < 256; ++i) DIGITS[i] = && err;
#if Alternate
#define DECU64DIGITS(n) \
        DIGITS[ n+1 ] = && c##n
        DECU64DIGITS(19);
        DECU64DIGITS(18);
        DECU64DIGITS(17);
        DECU64DIGITS(16);
        DECU64DIGITS(15);
        DECU64DIGITS(14);
        DECU64DIGITS(13);
        DECU64DIGITS(12);
        DECU64DIGITS(11);
        DECU64DIGITS(10);
        DECU64DIGITS(9);
        DECU64DIGITS(8);
        DECU64DIGITS(7);
        DECU64DIGITS(6);
        DECU64DIGITS(5);
        DECU64DIGITS(4);
        DECU64DIGITS(3);
        DECU64DIGITS(2);
        DECU64DIGITS(1);
        DECU64DIGITS(0);
#else
        DIGITS[20] = && c19;
        DIGITS[19] = && c18;
        DIGITS[18] = && c17;
        DIGITS[17] = && c16;
        DIGITS[16] = && c15;
        DIGITS[15] = && c14;
        DIGITS[14] = && c13;
        DIGITS[13] = && c12;
        DIGITS[12] = && c11;
        DIGITS[11] = && c10;
        DIGITS[10] = && c09;
        DIGITS[9] = && c08;
        DIGITS[8] = && c07;
        DIGITS[7] = && c06;
        DIGITS[6] = && c05;
        DIGITS[5] = && c04;
        DIGITS[4] = && c03;
        DIGITS[3] = && c02;
        DIGITS[2] = && c01;
        DIGITS[1] = && c00;
#endif

        goto run;
#endif
                }

#ifdef LETTVIN_LEXERS_H_CPP_UNIT
            bool UnitTestShow(const char *t, const size_t digits) {
                /// Efficiency not a premium in unit test service function.
                /// So code for outputting no more than 20 digits is clumsy.
                if (digits > 20) {
                    std::cout <<
                        "Illegal request for digit count > 20" <<
                        std::endl;
                    return true;
                } else if (digits == 0) {
                    std::cout <<
                        "Illegal request for digit count == 0" <<
                        std::endl;
                    return true;
                } else {
                    char c = 0;
                    size_t i, j;
                    std::string spaces(21 - digits, ' ');  ///< 1 extra space
                    std::cout << spaces;
                    /// Output characters as long as valid and fill 20 cols.
                    for (i = j = 0; j < digits; i += !!c, ++j) {
                        std::cout << ((c = t[i]) ? c : ' ');
                    }
                    return false;
                }
            }
            void UnitTest(
                    const char * s,
                    size_t digits = 20,
                    const u64t hi = top,
                    const u64t lo = zip ) {
                u64t error = zip;
                u64t ull;
                char buffer[32];
                strcpy(buffer, s);  // NOLINT
                char *t = buffer;

                /// 1) Output ASCII representation as given as 21 characters.
                if (UnitTestShow(t, digits)) return;
                (*this)(ull, t, error, digits, hi, lo);
                /// 2) Output the remaining characters after the lex.
                /// 3) Output the converted number after the lex.
                /// 4) Output the number of characters converted.
                /// 5) Output the error flag (1 or 0)
                /// The style of output will resemble these two lines
                /// IN                    BAD                   OUT  N E
                /// 18446744073709551616  18446744073709551616  0    0 1
                if (UnitTestShow(t, digits)) return;
                std::cout <<
                    std::setw(21) <<        ull << " " <<
                    std::setw(2)  << (t-buffer) << " " <<
                    error <<
                    std::endl;
            }

            void UnitTest(const u64t &val) {
                std::stringstream ss;
                ss << val; UnitTest(ss.str().c_str(), ss.str().size());
            }

            void UnitTest() {
                const char * test[] = {
                    "0",
                    "1",
                    "2",
                    "10",
                    "900",
                    "8000",
                    "70000",
                    "600000",
                    "5000000",
                    "40000000",
                    "300000000",
                    "2000000000",
                    "10000000000",
                    "900000000000",
                    "8000000000000",
                    "70000000000000",
                    "600000000000000",
                    "5000000000000000",
                    "40000000000000000",
                    "300000000000000000",
                    "2000000000000000000",
                    "10000000000000000000",   ///< good
                    "18446744073709551615",   ///< good (one less than bad)
                    "18446744073709551616",   ///< bad, too high value
                    "20000000000000000000",   ///< bad, too high value
                    "300000000000000000000",  ///< bad, too many digits
                    "",                       ///< bad, too  few digits
                    0L                        /// terminate with null ptr
                };

                std::cout <<
                    std::setw(21) <<  "IN" <<
                    std::setw(21) << "BAD" <<
                    std::setw(21) << "OUT" <<
                    "  N E" << std::endl;

                for (size_t i = 0; test[i]; ++i) {
                    UnitTest(test[i], strlen(test[i]));
                }
                UnitTest(test[2], strlen(test[2]), top, 3ULL);

                u64t val;
                val  = top; UnitTest(val);
                val += one; UnitTest(val);
                val -= one; UnitTest(val);
                val  = zip; UnitTest(val);
                val -= one; UnitTest(val);   ///< This wraps around.  No error.
                val += one; UnitTest(val);
            }
#endif

 private:
            ///################################################################
            static const u64t zip =  0ULL;
            static const u64t one =  1ULL;
            static const u64t ten = 10ULL;
            static const u64t top = 0xFFFFFFFFFFFFFFFFULL;

            static const u64t p0 =      one;
            static const u64t p1 =      ten;
            static const u64t p2 = p1 * ten;
            static const u64t p3 = p2 * ten;
            static const u64t p4 = p3 * ten;
            static const u64t p5 = p4 * ten;
            static const u64t p6 = p5 * ten;
            static const u64t p7 = p6 * ten;
            static const u64t p8 = p7 * ten;
            static const u64t p9 = p8 * ten;
            static const u64t pA = p9 * ten;
            static const u64t pB = pA * ten;
            static const u64t pC = pB * ten;
            static const u64t pD = pC * ten;
            static const u64t pE = pD * ten;
            static const u64t pF = pE * ten;
            static const u64t pG = pF * ten;
            static const u64t pH = pG * ten;
            static const u64t pI = pH * ten;
            static const u64t pJ = pI * ten;

            static const bool inv[ 20 ][ 256 ];  ///< Invalid character table
            static const u64t col[ 20 ][ 256 ];  ///< column-value lookup table
};

    /// PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    /// These defines are used to fill the col table with BAD values
#define B00000010(x) x, x
#define B00000100(x) B00000010(x), B00000010(x)
#define B00001000(x) B00000100(x), B00000100(x)
#define B00010000(x) B00001000(x), B00001000(x)
#define B00100000(x) B00010000(x), B00010000(x)
#define B01000000(x) B00100000(x), B00100000(x)
#define B10000000(x) B01000000(x), B01000000(x)
#define B00110000(x)  \
    B00100000(x), \
    B00010000(x)
#define B11000110(x)  \
    B10000000(x), \
    B01000000(x), \
    B00000100(x), \
    B00000010(x)
#define Bad48   B00110000(zip)
#define Bad198  B11000110(zip)
#define True48  B00110000(false)
#define True198 B11000110(false)

    ///########################################################################
    /// Table of digit validity for each column
    const bool lexDecU64t::inv[ 20 ][ 256 ] = {
#if Alternate
#define DECU64INVTABLE(a) \
        { True48, false, false, B00001000(a), True198}
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(false),
        DECU64INVTABLE(true)    ///< highest column has limited digits
#else
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(false), True198},
        { True48, false, false, B00001000(true),  True198}
#endif
    };

    ///########################################################################
    /// Table of summable value for each column
    const u64t lexDecU64t::col[ 20 ][ 256 ] = {
#if Alternate
#define DECU64COLTABLE(n) \
        { Bad48, 0, \
            1*p##n, 2*p##n, 3*p##n, 4*p##n, 5*p##n, \
            6*p##n, 7*p##n, 8*p##n, 9*p##n, Bad198}
        DECU64COLTABLE(0),
        DECU64COLTABLE(1),
        DECU64COLTABLE(2),
        DECU64COLTABLE(3),
        DECU64COLTABLE(4),
        DECU64COLTABLE(5),
        DECU64COLTABLE(6),
        DECU64COLTABLE(7),
        DECU64COLTABLE(8),
        DECU64COLTABLE(9),
        DECU64COLTABLE(A),
        DECU64COLTABLE(B),
        DECU64COLTABLE(C),
        DECU64COLTABLE(D),
        DECU64COLTABLE(E),
        DECU64COLTABLE(F),
        DECU64COLTABLE(G),
        DECU64COLTABLE(H),
        DECU64COLTABLE(I),
        DECU64COLTABLE(J)
#else
#define BAD48L(L) \
        { Bad48, 0, \
            1*p##L, 2*p##L, 3*p##L, 4*p##L, 5*p##L, \
            6*p##L, 7*p##L, 8*p##L, 9*p##L, Bad198 }
            BAD48L(0),
        BAD48L(1),
        BAD48L(2),
        BAD48L(3),
        BAD48L(4),
        BAD48L(5),
        BAD48L(6),
        BAD48L(7),
        BAD48L(8),
        BAD48L(9),
        BAD48L(A),
        BAD48L(B),
        BAD48L(C),
        BAD48L(D),
        BAD48L(E),
        BAD48L(F),
        BAD48L(G),
        BAD48L(H),
        BAD48L(I),
        BAD48L(J)
#endif
};

    static lexDecU64t lexDecU64_Instance;
}  // namespace Lettvin

#ifdef LETTVIN_LEXERS_H_CPP_UNIT
///****************************************************************************
int main(int argc, char *argv[]) {
  int retval = 1;
  const char *whoami = __FILE__ " " __DATE__ " " __TIME__ " ";

  std::cout <<
    whoami <<
    "UNIT TEST: starts " <<
    (Alternate?"Alternate style":"Basic style") <<
    std::endl;

  try {
    CONFIRM_DATA_SIZES;
    Lettvin::lexDecU64_Instance.UnitTest();
    retval = 0;
  }
#if 0
  catch(domain_error & e) {
    std::cerr << std::string("domain_error: ") + e.what() << std::endl;
  }
  catch(std::invalid_argument & e) {
    std::cerr << std::string("invalid_argument: ") + e.what() << std::endl;
  }
  catch(std::length_error & e) {
    std::cerr << std::string("length_error: ") + e.what() << std::endl;
  }
  catch(std::out_of_range & e) {
    std::cerr << std::string("out_of_range: ") + e.what() << std::endl;
  }
  catch(std::bad_cast & e) {
    std::cerr << std::string("bad_cast: ") + e.what() << std::endl;
  }
  catch(std::bad_typeid & e) {
    std::cerr << std::string("bad_typeid: ") + e.what() << std::endl;
  }
  catch(std::range_error & e) {
    std::cerr << std::string("range_error: ") + e.what() << std::endl;
  }
  catch(std::overflow_error & e) {
    std::cerr << std::string("overflow_error: ") + e.what() << std::endl;
  }
  catch(std::underflow_error & e) {
    std::cerr << std::string("underflow_error: ") + e.what() << std::endl;
  }
  catch(std::bad_alloc & e) {
    std::cerr << std::string("bad_alloc: ") + e.what() << std::endl;
  }
  catch(std::logic_error & e) {
    std::cerr << std::string("logic_error: ") + e.what() << std::endl;
  }
  catch(std::runtime_error & e) {
    std::cerr << std::string("runtime_error: ") + e.what() << std::endl;
  }
#endif
  catch(std::exception & e) {
    std::cerr <<
      whoami <<
      std::string("generic exept: ") + e.what() <<
      std::endl;
  }
  catch( Lettvin::s08pr s ) {                   ///< catch known errors
    std::cout << whoami << "Error: " << s << std::endl;
  }
  catch( const std::string &s ) {               ///< catch known errors
    std::cout << whoami << "Error: " << s << std::endl;
  }
  catch( ... ) {                                ///< catch unknown errors
    std::cout << whoami << "Error: unknown" << std::endl;
  }

  std::cout <<
    whoami <<
    "UNIT TEST: ends " <<
    (Alternate?"Alternate style":"Basic style") <<
    std::endl;


  return retval;
}

#endif  // LETTVIN_LEXERS_H_CPP_UNIT
#endif  // LETTVIN_LEXERS_H_CPP
/// ***************************************************************************
/// goto_test.h.cpp EOF
/// ***************************************************************************
