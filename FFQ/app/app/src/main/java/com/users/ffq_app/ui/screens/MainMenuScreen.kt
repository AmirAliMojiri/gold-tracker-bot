package com.users.ffq_app.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ExitToApp
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.R
import com.users.ffq_app.data.model.LocalAppStrings
import com.users.ffq_app.ui.navigation.Screen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainMenuScreen(
    onNavigate: (Screen) -> Unit,
    onExitApp: () -> Unit,
    onLogout: () -> Unit
) {
    val strings = LocalAppStrings.current
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(strings.mainMenu, fontWeight = FontWeight.Bold) },
                actions = {
                    IconButton(onClick = onLogout) {
                        Icon(Icons.AutoMirrored.Filled.ExitToApp, contentDescription = strings.logout)
                    }
                    IconButton(onClick = onExitApp) {
                        Icon(Icons.Default.PowerSettingsNew, contentDescription = strings.exitApp, tint = Color.Red)
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Surface(
                shape = CircleShape,
                shadowElevation = 6.dp,
                color = Color(0xFFFEFAEE),
                modifier = Modifier.size(110.dp)
            ) {
                Image(
                    painter = painterResource(id = R.drawable.my_logo),
                    contentDescription = strings.appName,
                    modifier = Modifier.fillMaxSize()
                )
            }
            Spacer(Modifier.height(12.dp))
            Text(
                text = strings.appName,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(Modifier.height(32.dp))

            MainMenuButton(
                text = strings.btnRegistration,
                subtitle = "ثبت اطلاعات بالینی، دموگرافیک و شاخص‌ها",
                icon = Icons.Default.PersonAdd,
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                onNavigate(Screen.Registration())
            }

            Spacer(Modifier.height(16.dp))

            MainMenuButton(
                text = strings.btnHistory,
                subtitle = "مشاهده پرونده‌ها و نتایج FFQ ثبت‌شده",
                icon = Icons.AutoMirrored.Filled.List,
                containerColor = MaterialTheme.colorScheme.secondary
            ) {
                onNavigate(Screen.History)
            }

            Spacer(Modifier.height(16.dp))

            MainMenuButton(
                text = strings.btnContactUs,
                subtitle = "ارتباط با تیم توسعه و پشتیبانی",
                icon = Icons.Default.Call,
                containerColor = MaterialTheme.colorScheme.tertiary
            ) {
                onNavigate(Screen.ContactUs)
            }
        }
    }
}

@Composable
fun MainMenuButton(
    text: String,
    subtitle: String,
    icon: ImageVector,
    containerColor: Color,
    onClick: () -> Unit
) {
    Button(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .height(72.dp),
        shape = RoundedCornerShape(16.dp),
        colors = ButtonDefaults.buttonColors(containerColor = containerColor)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(imageVector = icon, contentDescription = null, modifier = Modifier.size(28.dp))
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(text = text, fontSize = 17.sp, fontWeight = FontWeight.Bold)
                Text(text = subtitle, fontSize = 12.sp, color = Color.White.copy(alpha = 0.85f))
            }
            Icon(Icons.Default.ChevronLeft, contentDescription = null)
        }
    }
}
