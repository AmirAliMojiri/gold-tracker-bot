package com.users.ffq_app.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.NoteAdd
import androidx.compose.material.icons.filled.Save
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.data.model.FFQAnswer
import com.users.ffq_app.data.model.FFQItem
import com.users.ffq_app.data.model.LocalAppStrings
import com.users.ffq_app.data.model.PatientRecord
import com.users.ffq_app.data.model.RegistrationData
import com.users.ffq_app.util.FFQRepository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FFQQuestionnaireScreen(
    patientId: String,
    registrationData: RegistrationData,
    initialAnswers: Map<Int, FFQAnswer> = emptyMap(),
    onNavigateBack: () -> Unit,
    onSaveSuccess: () -> Unit
) {
    val context = LocalContext.current
    val strings = LocalAppStrings.current
    val allItems = remember { FFQRepository.loadFFQItems(context) }
    var searchQuery by remember { mutableStateOf("") }
    var answersMap by remember { mutableStateOf(initialAnswers.toMutableMap()) }

    val filteredItems = remember(searchQuery, allItems) {
        if (searchQuery.isBlank()) allItems
        else allItems.filter { it.name.contains(searchQuery.trim(), ignoreCase = true) || it.id.toString() == searchQuery.trim() }
    }

    val filledCount = answersMap.values.count { !it.isEmpty() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("پرسشنامه بسامد خوراک (۱۴۷ آیتم)", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text("شناسه بیمار: $patientId ($filledCount از ۱۴۷ تکمیل‌شده)", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = strings.back)
                    }
                },
                actions = {
                    IconButton(onClick = {
                        val record = PatientRecord(
                            patientId = patientId,
                            registration = registrationData,
                            answers = answersMap
                        )
                        val success = FFQRepository.saveRecord(context, record)
                        if (success) {
                            Toast.makeText(context, strings.successSaved, Toast.LENGTH_SHORT).show()
                            onSaveSuccess()
                        } else {
                            Toast.makeText(context, "خطا در ذخیره اطلاعات", Toast.LENGTH_SHORT).show()
                        }
                    }) {
                        Icon(Icons.Default.Save, contentDescription = strings.save, tint = MaterialTheme.colorScheme.primary)
                    }
                }
            )
        },
        bottomBar = {
            Surface(
                shadowElevation = 8.dp,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("تعداد پاسخ‌ها: $filledCount / ۱۴۷", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        val pct = if (allItems.isNotEmpty()) (filledCount * 100) / allItems.size else 0
                        Text("$pct% تکمیل شده", fontSize = 12.sp, color = Color.Gray)
                    }
                    Button(
                        onClick = {
                            val record = PatientRecord(
                                patientId = patientId,
                                registration = registrationData,
                                answers = answersMap
                            )
                            val success = FFQRepository.saveRecord(context, record)
                            if (success) {
                                Toast.makeText(context, strings.successSaved, Toast.LENGTH_SHORT).show()
                                onSaveSuccess()
                            } else {
                                Toast.makeText(context, "خطا در ذخیره پرونده", Toast.LENGTH_SHORT).show()
                            }
                        },
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Default.Check, null)
                        Spacer(Modifier.width(8.dp))
                        Text("ذخیره نهایی پرونده")
                    }
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 12.dp)
        ) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                label = { Text("جستجوی نام ماده غذایی یا شماره ردیف...") },
                leadingIcon = { Icon(Icons.Default.Search, null) },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            )

            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(10.dp),
                contentPadding = PaddingValues(bottom = 16.dp)
            ) {
                itemsIndexed(filteredItems, key = { _, item -> item.id }) { _, item ->
                    val curAnswer = answersMap[item.id] ?: FFQAnswer()
                    FFQItemCard(
                        item = item,
                        answer = curAnswer,
                        onAnswerChange = { newAns ->
                            val updated = answersMap.toMutableMap()
                            if (newAns.isEmpty()) {
                                updated.remove(item.id)
                            } else {
                                updated[item.id] = newAns
                            }
                            answersMap = updated
                        }
                    )
                }
            }
        }
    }
}

private fun formatFreq(value: Double): String {
    if (value <= 0.0) return ""
    val rounded = Math.round(value * 100.0) / 100.0
    return if (rounded % 1.0 == 0.0) {
        rounded.toLong().toString()
    } else {
        String.format(java.util.Locale.US, "%.2f", rounded).trimEnd('0').trimEnd('.')
    }
}

@Composable
fun FFQItemCard(
    item: FFQItem,
    answer: FFQAnswer,
    onAnswerChange: (FFQAnswer) -> Unit
) {
    val isAnswered = !answer.isEmpty()
    var showNotesField by remember { mutableStateOf(answer.userNotes.isNotBlank()) }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isAnswered) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.25f)
            else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            // Header Row: Item Name and Portion
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "${item.id}. ${item.name}",
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.weight(1f)
                )
                Spacer(Modifier.width(8.dp))
                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.7f)
                ) {
                    Text(
                        text = "واحد: ${item.portion}",
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp),
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }

            // Standard Notes (if present from original questionnaire protocol)
            if (item.notes.isNotBlank()) {
                Surface(
                    shape = RoundedCornerShape(6.dp),
                    color = MaterialTheme.colorScheme.surface.copy(alpha = 0.6f),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 4.dp)
                ) {
                    Text(
                        text = "ملاحظات پروتکل: ${item.notes}",
                        fontSize = 11.sp,
                        color = Color.DarkGray,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                    )
                }
            }

            Spacer(Modifier.height(8.dp))
            Text("بسامد مصرف بر اساس واحد فوق (تکمیل یکی، سایر مقادیر را محاسبه می‌کند):", fontSize = 11.sp, color = Color.Gray)
            Spacer(Modifier.height(4.dp))

            // 4 Frequency Inputs with auto-calculation
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                // Day
                FrequencyInput(
                    label = "روز",
                    value = answer.day,
                    modifier = Modifier.weight(1f)
                ) { input ->
                    if (input.isBlank()) {
                        onAnswerChange(FFQAnswer(userNotes = answer.userNotes))
                    } else {
                        val d = input.toDoubleOrNull()
                        if (d != null && d >= 0) {
                            val w = formatFreq(d * 7.0)
                            val m = formatFreq(d * 30.42)
                            val y = formatFreq(d * 365.0)
                            onAnswerChange(FFQAnswer(day = input, week = w, month = m, year = y, userNotes = answer.userNotes))
                        } else {
                            onAnswerChange(answer.copy(day = input))
                        }
                    }
                }

                // Week
                FrequencyInput(
                    label = "هفته",
                    value = answer.week,
                    modifier = Modifier.weight(1f)
                ) { input ->
                    if (input.isBlank()) {
                        onAnswerChange(FFQAnswer(userNotes = answer.userNotes))
                    } else {
                        val w = input.toDoubleOrNull()
                        if (w != null && w >= 0) {
                            val d = formatFreq(w / 7.0)
                            val m = formatFreq(w * 4.345)
                            val y = formatFreq(w * 52.14)
                            onAnswerChange(FFQAnswer(day = d, week = input, month = m, year = y, userNotes = answer.userNotes))
                        } else {
                            onAnswerChange(answer.copy(week = input))
                        }
                    }
                }

                // Month
                FrequencyInput(
                    label = "ماه",
                    value = answer.month,
                    modifier = Modifier.weight(1f)
                ) { input ->
                    if (input.isBlank()) {
                        onAnswerChange(FFQAnswer(userNotes = answer.userNotes))
                    } else {
                        val m = input.toDoubleOrNull()
                        if (m != null && m >= 0) {
                            val d = formatFreq(m / 30.42)
                            val w = formatFreq(m / 4.345)
                            val y = formatFreq(m * 12.0)
                            onAnswerChange(FFQAnswer(day = d, week = w, month = input, year = y, userNotes = answer.userNotes))
                        } else {
                            onAnswerChange(answer.copy(month = input))
                        }
                    }
                }

                // Year (User specific requirement: filling year computes month, week, day)
                FrequencyInput(
                    label = "سال",
                    value = answer.year,
                    modifier = Modifier.weight(1f)
                ) { input ->
                    if (input.isBlank()) {
                        onAnswerChange(FFQAnswer(userNotes = answer.userNotes))
                    } else {
                        val y = input.toDoubleOrNull()
                        if (y != null && y >= 0) {
                            val m = formatFreq(y / 12.0)
                            val w = formatFreq(y / 52.14)
                            val d = formatFreq(y / 365.0)
                            onAnswerChange(FFQAnswer(day = d, week = w, month = m, year = input, userNotes = answer.userNotes))
                        } else {
                            onAnswerChange(answer.copy(year = input))
                        }
                    }
                }
            }

            Spacer(Modifier.height(8.dp))

            // Notes Button & Section (User specific requirement: option to add/edit considerations)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedButton(
                    onClick = { showNotesField = !showNotesField },
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = if (answer.userNotes.isNotBlank()) MaterialTheme.colorScheme.primary else Color(0xFF444444)
                    ),
                    contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                    modifier = Modifier.height(36.dp)
                ) {
                    Icon(
                        if (answer.userNotes.isNotBlank()) Icons.Default.EditNote else Icons.Default.NoteAdd,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(Modifier.width(6.dp))
                    Text(
                        if (answer.userNotes.isNotBlank()) "ویرایش ملاحظات"
                        else if (item.notes.isNotBlank()) "+ ثبت ملاحظات (${item.notes.take(18)}...)"
                        else "+ افزودن ملاحظات این آیتم",
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Medium
                    )
                }

                if (answer.userNotes.isNotBlank() && !showNotesField) {
                    Text(
                        text = "ملاحظات: ${answer.userNotes}",
                        fontSize = 11.sp,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        modifier = Modifier
                            .weight(1f, fill = false)
                            .padding(start = 8.dp)
                    )
                }
            }

            // Expandable Notes input field
            if (showNotesField) {
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = answer.userNotes,
                    onValueChange = { onAnswerChange(answer.copy(userNotes = it)) },
                    label = { Text("ملاحظات اختصاصی بیمار برای این غذا", fontSize = 11.sp) },
                    placeholder = {
                        Text(
                            if (item.notes.isNotBlank()) item.notes
                            else "مثال: نوع، مارک تجاری، روش پخت، چربی یا فصل مصرف...",
                            fontSize = 11.sp
                        )
                    },
                    singleLine = false,
                    maxLines = 3,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }
    }
}

@Composable
fun FrequencyInput(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
    onValueChange: (String) -> Unit
) {
    OutlinedTextField(
        value = value,
        onValueChange = { onValueChange(it) },
        label = { Text(label, fontSize = 11.sp) },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
        singleLine = true,
        modifier = modifier
    )
}
