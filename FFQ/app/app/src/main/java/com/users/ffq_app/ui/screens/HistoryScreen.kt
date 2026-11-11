package com.users.ffq_app.ui.screens

import android.widget.Toast
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.DeleteOutline
import androidx.compose.material.icons.filled.FileDownload
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.TableChart
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.data.model.LocalAppStrings
import com.users.ffq_app.data.model.PatientRecord
import com.users.ffq_app.util.ExcelExporter
import com.users.ffq_app.util.FFQRepository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(
    onPatientSelected: (String) -> Unit,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    val strings = LocalAppStrings.current
    var records by remember { mutableStateOf<List<PatientRecord>>(emptyList()) }
    var searchQuery by remember { mutableStateOf("") }
    var selectionMode by remember { mutableStateOf(false) }
    var selectedIds by remember { mutableStateOf(setOf<String>()) }
    var showDeleteConfirm by remember { mutableStateOf(false) }
    var showExportDialog by remember { mutableStateOf(false) }

    fun refresh() {
        records = FFQRepository.getAllRecords(context)
    }

    LaunchedEffect(Unit) {
        refresh()
    }

    val filteredRecords = remember(searchQuery, records) {
        if (searchQuery.isBlank()) records
        else records.filter { it.patientId.contains(searchQuery.trim(), ignoreCase = true) }
    }

    // Export Dialog
    if (showExportDialog) {
        val targetRecords = if (selectionMode && selectedIds.isNotEmpty()) {
            records.filter { selectedIds.contains(it.patientId) }
        } else {
            records
        }

        AlertDialog(
            onDismissRequest = { showExportDialog = false },
            title = { Text("انتخاب نوع خروجی اکسل (${targetRecords.size} پرونده)") },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("کدام فایل اکسل را می‌خواهید دریافت و مشاهده کنید؟", fontSize = 13.sp)

                    Button(
                        onClick = {
                            showExportDialog = false
                            try {
                                val file = ExcelExporter.exportRegistrationExcel(
                                    context = context,
                                    records = targetRecords,
                                    customFileName = "اطلاعات_ثبت_نام_کلیه_بیماران.xlsx"
                                )
                                Toast.makeText(context, "فایل اکسل مشخصات و IPAQ ایجاد شد", Toast.LENGTH_SHORT).show()
                                ExcelExporter.openOrShareFile(context, file, "اکسل مشخصات و IPAQ بیماران")
                            } catch (e: Exception) {
                                Toast.makeText(context, "خطا: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("خروجی ۱: جدول ثبت‌نام و IPAQ (۵۲ ستون)")
                    }

                    FilledTonalButton(
                        onClick = {
                            showExportDialog = false
                            try {
                                val allItems = FFQRepository.loadFFQItems(context)
                                val file = ExcelExporter.exportAllPatientsNutrientSummary(
                                    context = context,
                                    records = targetRecords,
                                    allItems = allItems,
                                    customFileName = "خلاصه_مواد_مغذی_کلیه_بیماران.xlsx"
                                )
                                Toast.makeText(context, "فایل اکسل خلاصه مواد مغذی ایجاد شد", Toast.LENGTH_SHORT).show()
                                ExcelExporter.openOrShareFile(context, file, "اکسل خلاصه دریافتی مواد مغذی کلیه بیماران")
                            } catch (e: Exception) {
                                Toast.makeText(context, "خطا: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text("خروجی ۲: ماتریس تحلیل ۶۳ ماده مغذی بیماران")
                    }
                }
            },
            confirmButton = {},
            dismissButton = {
                TextButton(onClick = { showExportDialog = false }) {
                    Text("انصراف")
                }
            }
        )
    }

    if (showDeleteConfirm) {
        AlertDialog(
            onDismissRequest = { showDeleteConfirm = false },
            title = { Text(strings.deleteSelected) },
            text = { Text(strings.deleteConfirm) },
            confirmButton = {
                Button(onClick = {
                    showDeleteConfirm = false
                    FFQRepository.deleteRecords(context, selectedIds)
                    selectionMode = false
                    selectedIds = emptySet()
                    refresh()
                    Toast.makeText(context, "پرونده‌های انتخابی حذف شدند", Toast.LENGTH_SHORT).show()
                }) { Text(strings.yes) }
            },
            dismissButton = {
                OutlinedButton(onClick = { showDeleteConfirm = false }) { Text(strings.no) }
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        if (selectionMode) "${selectedIds.size} مورد انتخاب شده"
                        else strings.btnHistory,
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    if (selectionMode) {
                        IconButton(onClick = { selectionMode = false; selectedIds = emptySet() }) {
                            Icon(Icons.Default.Close, null)
                        }
                    } else {
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = strings.back)
                        }
                    }
                },
                actions = {
                    // Excel Export Action
                    IconButton(onClick = {
                        if (records.isEmpty()) {
                            Toast.makeText(context, "هنوز پرونده‌ای برای خروجی اکسل وجود ندارد", Toast.LENGTH_SHORT).show()
                        } else {
                            showExportDialog = true
                        }
                    }) {
                        Icon(Icons.Default.FileDownload, contentDescription = "خروجی اکسل", tint = MaterialTheme.colorScheme.primary)
                    }

                    if (selectionMode) {
                        IconButton(onClick = { if (selectedIds.isNotEmpty()) showDeleteConfirm = true }) {
                            Icon(Icons.Default.Delete, null, tint = Color.Red)
                        }
                    } else {
                        IconButton(onClick = { selectionMode = true }) {
                            Icon(Icons.Default.DeleteOutline, null)
                        }
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp)
        ) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                label = { Text("جستجو بر اساس شناسه بیمار (ID)...") },
                leadingIcon = { Icon(Icons.Default.Search, null) },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            )

            if (filteredRecords.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(strings.noRecords, color = Color.Gray, fontSize = 16.sp)
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(bottom = 16.dp)
                ) {
                    items(filteredRecords, key = { it.patientId }) { record ->
                        val isSelected = selectedIds.contains(record.patientId)
                        val reg = record.registration
                        val answeredCount = record.answers.values.count { !it.isEmpty() }

                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    if (selectionMode) {
                                        selectedIds = if (isSelected) selectedIds - record.patientId else selectedIds + record.patientId
                                    } else {
                                        onPatientSelected(record.patientId)
                                    }
                                },
                            shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(
                                containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f)
                                else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f)
                            )
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(14.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                if (selectionMode) {
                                    Checkbox(
                                        checked = isSelected,
                                        onCheckedChange = { chk ->
                                            selectedIds = if (chk) selectedIds + record.patientId else selectedIds - record.patientId
                                        }
                                    )
                                    Spacer(Modifier.width(8.dp))
                                }

                                Column(modifier = Modifier.weight(1f)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text("شناسه: ${record.patientId}", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = MaterialTheme.colorScheme.primary)
                                        Text(FFQRepository.formatTimestamp(record.timestamp), fontSize = 12.sp, color = Color.Gray)
                                    }
                                    Spacer(Modifier.height(4.dp))
                                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                        if (reg.age.isNotBlank()) Text("سن: ${reg.age}", fontSize = 13.sp)
                                        reg.bmi?.let { Text(String.format("BMI: %.1f", it), fontSize = 13.sp, fontWeight = FontWeight.SemiBold) }
                                        Text(if (reg.gender == 1) "جنسیت: مرد" else "جنسیت: زن", fontSize = 13.sp)
                                    }
                                    Spacer(Modifier.height(4.dp))
                                    Text("آیتم‌های FFQ تکمیل‌شده: $answeredCount از ۱۴۷", fontSize = 12.sp, color = MaterialTheme.colorScheme.secondary)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
