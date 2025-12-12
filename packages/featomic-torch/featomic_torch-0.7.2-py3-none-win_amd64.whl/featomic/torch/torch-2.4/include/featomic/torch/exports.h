
#ifndef FEATOMIC_TORCH_EXPORT_H
#define FEATOMIC_TORCH_EXPORT_H

#ifdef FEATOMIC_TORCH_STATIC_DEFINE
#  define FEATOMIC_TORCH_EXPORT
#  define FEATOMIC_TORCH_NO_EXPORT
#else
#  ifndef FEATOMIC_TORCH_EXPORT
#    ifdef featomic_torch_EXPORTS
        /* We are building this library */
#      define FEATOMIC_TORCH_EXPORT __declspec(dllexport)
#    else
        /* We are using this library */
#      define FEATOMIC_TORCH_EXPORT __declspec(dllimport)
#    endif
#  endif

#  ifndef FEATOMIC_TORCH_NO_EXPORT
#    define FEATOMIC_TORCH_NO_EXPORT 
#  endif
#endif

#ifndef FEATOMIC_TORCH_DEPRECATED
#  define FEATOMIC_TORCH_DEPRECATED __declspec(deprecated)
#endif

#ifndef FEATOMIC_TORCH_DEPRECATED_EXPORT
#  define FEATOMIC_TORCH_DEPRECATED_EXPORT FEATOMIC_TORCH_EXPORT FEATOMIC_TORCH_DEPRECATED
#endif

#ifndef FEATOMIC_TORCH_DEPRECATED_NO_EXPORT
#  define FEATOMIC_TORCH_DEPRECATED_NO_EXPORT FEATOMIC_TORCH_NO_EXPORT FEATOMIC_TORCH_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef FEATOMIC_TORCH_NO_DEPRECATED
#    define FEATOMIC_TORCH_NO_DEPRECATED
#  endif
#endif

#endif /* FEATOMIC_TORCH_EXPORT_H */
