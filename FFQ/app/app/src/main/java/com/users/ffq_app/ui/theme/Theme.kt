package com.users.ffq_app.ui.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val LightColorScheme = lightColorScheme(
    primary = PastelGreenPrimary,
    onPrimary = Color.White,
    primaryContainer = PastelGreenContainer,
    onPrimaryContainer = PastelGreenOnContainer,
    secondary = PastelSageSecondary,
    onSecondary = Color.White,
    secondaryContainer = PastelSageContainer,
    onSecondaryContainer = PastelSageOnContainer,
    tertiary = PastelMintTertiary,
    onTertiary = Color.White,
    tertiaryContainer = PastelMintContainer,
    onTertiaryContainer = PastelMintOnContainer,
    background = LightBackground,
    onBackground = Color(0xFF1B1F17),
    surface = SurfaceColor,
    onSurface = Color(0xFF1B1F17),
    surfaceVariant = SurfaceVariantColor,
    onSurfaceVariant = Color(0xFF424A3D),
    outline = OutlineColor,
    outlineVariant = OutlineVariantColor
)

private val DarkColorScheme = darkColorScheme(
    primary = PastelGreenDarkPrimary,
    onPrimary = Color(0xFF153802),
    primaryContainer = PastelGreenDarkContainer,
    onPrimaryContainer = PastelGreenDarkOnContainer,
    secondary = Color(0xFFBCCBB1),
    onSecondary = Color(0xFF273420),
    secondaryContainer = Color(0xFF3D4B35),
    onSecondaryContainer = Color(0xFFD8E7CC),
    tertiary = Color(0xFFA1D0C4),
    onTertiary = Color(0xFF08372F),
    background = DarkBackground,
    onBackground = Color(0xFFE2E4DC),
    surface = DarkSurface,
    onSurface = Color(0xFFE2E4DC),
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = Color(0xFFC4CDC0)
)

@Composable
fun FFQAppTheme(
    themeMode: String = "light",
    content: @Composable () -> Unit
) {
    val isSystemDark = isSystemInDarkTheme()
    val isDark = when (themeMode) {
        "dark" -> true
        "light" -> false
        else -> isSystemDark
    }
    val colorScheme = if (isDark) DarkColorScheme else LightColorScheme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
