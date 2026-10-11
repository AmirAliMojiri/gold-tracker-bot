package com.users.ffq_app.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.BuildConfig
import com.users.ffq_app.data.local.AppPrefs
import com.users.ffq_app.data.model.LocalAppStrings

@Composable
fun AdminLoginScreen(onSuccess: () -> Unit, onBack: () -> Unit) {
    var adminUser by remember { mutableStateOf("") }
    var adminPass by remember { mutableStateOf("") }
    val context = LocalContext.current
    val strings = LocalAppStrings.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            Icons.Default.AdminPanelSettings,
            contentDescription = null,
            modifier = Modifier.size(80.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Spacer(Modifier.height(16.dp))
        Text(strings.adminLoginTitle, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(32.dp))

        OutlinedTextField(
            value = adminUser,
            onValueChange = { adminUser = it },
            label = { Text(strings.adminUser) },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(16.dp))
        OutlinedTextField(
            value = adminPass,
            onValueChange = { adminPass = it },
            label = { Text(strings.adminPass) },
            visualTransformation = PasswordVisualTransformation(),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(32.dp))

        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            OutlinedButton(onClick = onBack, modifier = Modifier.weight(1f)) {
                Text(strings.back)
            }
            Button(
                onClick = {
                    if (adminUser == BuildConfig.ADMIN_USER && adminPass == BuildConfig.ADMIN_PASS) {
                        onSuccess()
                    } else {
                        Toast.makeText(context, strings.wrongAdminInfo, Toast.LENGTH_SHORT).show()
                    }
                },
                modifier = Modifier.weight(1f)
            ) {
                Text(strings.enterDashboard)
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AdminDashboardScreen(
    onBack: () -> Unit,
    onThemeModeChanged: (String) -> Unit = {}
) {
    val context = LocalContext.current
    val strings = LocalAppStrings.current
    var users by remember { mutableStateOf(AppPrefs.getUsers(context)) }
    var newUser by remember { mutableStateOf("") }
    var newPass by remember { mutableStateOf("") }

    var currentThemeMode by remember { mutableStateOf(AppPrefs.getThemeMode(context)) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(strings.adminDashboard) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = strings.back)
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            // Theme Mode Card
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "تنظیم تم برنامه (ظاهر)",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(Modifier.height(12.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        listOf(
                            Triple("light", "روشن (Light)", Icons.Default.LightMode),
                            Triple("dark", "تاریک (Dark)", Icons.Default.DarkMode),
                            Triple("system", "سیستم", Icons.Default.Settings)
                        ).forEach { (mode, label, icon) ->
                            FilterChip(
                                selected = currentThemeMode == mode,
                                onClick = {
                                    currentThemeMode = mode
                                    AppPrefs.setThemeMode(context, mode)
                                    onThemeModeChanged(mode)
                                },
                                label = { Text(label, fontSize = 12.sp) },
                                leadingIcon = { Icon(icon, contentDescription = null, modifier = Modifier.size(16.dp)) }
                            )
                        }
                    }
                }
            }

            Spacer(Modifier.height(16.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        strings.staffManagement,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary
                    )
                    Spacer(Modifier.height(16.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = newUser,
                            onValueChange = { newUser = it },
                            label = { Text(strings.newUserLabel) },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                        OutlinedTextField(
                            value = newPass,
                            onValueChange = { newPass = it },
                            label = { Text(strings.newPassLabel) },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                    }
                    Spacer(Modifier.height(12.dp))
                    Button(
                        onClick = {
                            if (newUser.isNotBlank() && newPass.isNotBlank()) {
                                val trimmedUser = newUser.trim()
                                val newList = users.filter { it.first != trimmedUser } + Pair(trimmedUser, newPass)
                                AppPrefs.saveUsers(context, newList)
                                users = newList
                                newUser = ""
                                newPass = ""
                                Toast.makeText(context, "کاربر با موفقیت ثبت شد", Toast.LENGTH_SHORT).show()
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Icon(Icons.Default.PersonAdd, null)
                        Spacer(Modifier.width(8.dp))
                        Text(strings.addStaff)
                    }
                }
            }

            Spacer(Modifier.height(24.dp))
            Text(
                "لیست کاربران تعریف‌شده (${users.size})",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(Modifier.height(12.dp))

            if (users.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(strings.noRecords, color = Color.Gray)
                }
            } else {
                users.forEach { userPair ->
                    UserAccountRow(
                        userPair = userPair,
                        onUpdate = { old, updated ->
                            val newList = users.toMutableList()
                            val idx = newList.indexOf(old)
                            if (idx != -1) {
                                newList[idx] = updated
                                AppPrefs.saveUsers(context, newList)
                                users = newList
                            }
                        },
                        onDelete = {
                            val newList = users.filter { it != userPair }
                            AppPrefs.saveUsers(context, newList)
                            users = newList
                        }
                    )
                    Divider(modifier = Modifier.padding(vertical = 4.dp))
                }
            }
        }
    }
}

@Composable
fun UserAccountRow(
    userPair: Pair<String, String>,
    onUpdate: (Pair<String, String>, Pair<String, String>) -> Unit,
    onDelete: () -> Unit
) {
    var isEditing by remember { mutableStateOf(false) }
    var editUser by remember { mutableStateOf(userPair.first) }
    var editPass by remember { mutableStateOf(userPair.second) }
    var passVisible by remember { mutableStateOf(false) }
    val strings = LocalAppStrings.current

    if (isEditing) {
        Column(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
            OutlinedTextField(
                value = editUser,
                onValueChange = { editUser = it },
                label = { Text(strings.username) },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = editPass,
                onValueChange = { editPass = it },
                label = { Text(strings.password) },
                modifier = Modifier.fillMaxWidth(),
                visualTransformation = if (passVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = { passVisible = !passVisible }) {
                        Icon(if (passVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff, null)
                    }
                }
            )
            Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                TextButton(onClick = { isEditing = false }) { Text(strings.cancel) }
                Spacer(Modifier.width(8.dp))
                Button(onClick = {
                    if (editUser.isNotBlank() && editPass.isNotBlank()) {
                        onUpdate(userPair, Pair(editUser.trim(), editPass))
                        isEditing = false
                    }
                }) { Text(strings.save) }
            }
        }
    } else {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(userPair.first, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(if (passVisible) userPair.second else "••••••••", color = Color.Gray, fontSize = 13.sp)
                    IconButton(onClick = { passVisible = !passVisible }, modifier = Modifier.size(24.dp)) {
                        Icon(if (passVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff, null, Modifier.size(16.dp))
                    }
                }
            }
            IconButton(onClick = { isEditing = true }) {
                Icon(Icons.Default.Edit, contentDescription = strings.edit, tint = MaterialTheme.colorScheme.primary)
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, contentDescription = strings.delete, tint = Color.Red)
            }
        }
    }
}
