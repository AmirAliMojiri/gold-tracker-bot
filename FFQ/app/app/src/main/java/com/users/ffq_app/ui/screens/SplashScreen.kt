package com.users.ffq_app.ui.screens

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.R
import com.users.ffq_app.data.model.LocalAppStrings
import kotlinx.coroutines.delay

@Composable
fun SplashScreen(onFinished: () -> Unit) {
    val strings = LocalAppStrings.current
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val scale by infiniteTransition.animateFloat(
        initialValue = 0.97f,
        targetValue = 1.03f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scale"
    )

    // Splash screen timer: 2.8 seconds of authentic XP loading experience
    LaunchedEffect(Unit) {
        delay(2800)
        onFinished()
    }

    // Windows XP classic pitch-black boot background
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF000000)),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.padding(horizontal = 24.dp)
        ) {
            // App Logo
            Surface(
                shape = CircleShape,
                shadowElevation = 12.dp,
                color = Color(0xFFFEFAEE),
                modifier = Modifier
                    .size(135.dp)
                    .scale(scale)
            ) {
                Image(
                    painter = painterResource(id = R.drawable.my_logo),
                    contentDescription = strings.appName,
                    modifier = Modifier.fillMaxSize()
                )
            }

            Spacer(modifier = Modifier.height(28.dp))

            // App Name (Crisp white with pastel green hint)
            Text(
                text = strings.appName,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                fontSize = 26.sp
            )

            Spacer(modifier = Modifier.height(6.dp))

            // Persian Subtitle
            Text(
                text = "سامانه جامع ارزیابی بسامد خوراک و داده‌های سلامت",
                style = MaterialTheme.typography.bodyMedium,
                color = Color(0xFFB0B7A8),
                fontSize = 13.sp
            )

            Spacer(modifier = Modifier.height(44.dp))

            // Iconic Windows XP Loading Bar (Track + 3 marching glossy pastel blocks)
            WindowsXpProgressBar()

            Spacer(modifier = Modifier.height(18.dp))

            Text(
                text = "در حال راه‌اندازی و بارگذاری داده‌ها...",
                style = MaterialTheme.typography.bodySmall,
                color = Color(0xFF717D67),
                fontSize = 12.sp
            )
        }

        // Bottom Footer
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "نرم‌افزار بالینی و پژوهشی تغذیه • نگارش ۱.۰",
                fontSize = 11.sp,
                color = Color(0xFF555F4D)
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = "Copyright © 2026 FFQ Health Assessment",
                fontSize = 10.sp,
                color = Color(0xFF404739)
            )
        }
    }
}

/**
 * Windows XP Classic Boot Loader Bar:
 * A dark metallic track with 3 glossy rectangular blocks marching across continuously.
 */
@Composable
fun WindowsXpProgressBar(
    modifier: Modifier = Modifier
) {
    val trackWidth = 176.dp
    val trackHeight = 15.dp
    val blockWidth = 9.dp
    val blockHeight = 11.dp
    val blockSpacing = 2.5.dp

    val transition = rememberInfiniteTransition(label = "xp_loader")
    // Animates the offset from before the left edge to past the right edge
    val animProgress by transition.animateFloat(
        initialValue = -0.35f,
        targetValue = 1.35f,
        animationSpec = infiniteRepeatable(
            animation = tween(1250, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "xp_progress"
    )

    // Outer track with dark metallic border
    Box(
        modifier = modifier
            .width(trackWidth)
            .height(trackHeight)
            .clip(RoundedCornerShape(3.dp))
            .background(Color(0xFF000000))
            .border(1.5.dp, Color(0xFF4A4E46), RoundedCornerShape(3.dp))
            .padding(1.5.dp)
            .clipToBounds()
    ) {
        BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
            val totalWidthPx = constraints.maxWidth.toFloat()
            val xOffset = animProgress * totalWidthPx

            Row(
                modifier = Modifier
                    .offset { IntOffset(xOffset.toInt(), 0) }
                    .align(Alignment.CenterStart),
                horizontalArrangement = Arrangement.spacedBy(blockSpacing)
            ) {
                repeat(3) {
                    // Windows XP glossy 3D block
                    Box(
                        modifier = Modifier
                            .width(blockWidth)
                            .height(blockHeight)
                            .clip(RoundedCornerShape(2.dp))
                            .background(
                                Brush.verticalGradient(
                                    listOf(
                                        Color(0xFFB4F285), // Soft pastel top highlight
                                        Color(0xFF5E9434), // Core brand pastel green
                                        Color(0xFF285012)  // Deep shadow at base
                                    )
                                )
                            )
                            .border(0.5.dp, Color.White.copy(alpha = 0.45f), RoundedCornerShape(2.dp))
                    )
                }
            }
        }
    }
}
