package com.users.ffq_app.ui.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.RestaurantMenu
import androidx.compose.material.icons.filled.Share
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
import com.users.ffq_app.data.model.RegistrationData
import com.users.ffq_app.util.ExcelExporter
import com.users.ffq_app.util.FFQRepository

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PatientDetailScreen(
    patientId: String,
    onNavigateBack: () -> Unit,
    onEditRegistration: (RegistrationData) -> Unit,
    onOpenFFQ: (PatientRecord) -> Unit
) {
    val context = LocalContext.current
    val strings = LocalAppStrings.current
    var record by remember { mutableStateOf<PatientRecord?>(null) }
    val allItems = remember { FFQRepository.loadFFQItems(context) }

    LaunchedEffect(patientId) {
        record = FFQRepository.getRecord(context, patientId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("جزئیات پرونده بیمار ($patientId)", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = strings.back)
                    }
                }
            )
        }
    ) { innerPadding ->
        val currentRecord = record
        if (currentRecord == null) {
            Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                Text("در حال بارگذاری...")
            }
        } else {
            val reg = currentRecord.registration
            val answers = currentRecord.answers
            val answeredCount = answers.values.count { !it.isEmpty() }

            // Calculate key nutrient intakes
            val nutrientTotals = remember(currentRecord, allItems) {
                val totals = mutableMapOf<String, Double>()
                for (item in allItems) {
                    val ans = answers[item.id] ?: continue
                    val mult = ans.toDailyMultiplier()
                    if (mult <= 0) continue
                    for ((k, v) in item.nutrients) {
                        totals[k] = (totals[k] ?: 0.0) + (mult * v)
                    }
                }
                totals
            }

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .padding(16.dp)
                    .verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Header Actions (Edit Registration / Edit FFQ)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = { onOpenFFQ(currentRecord) },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Default.RestaurantMenu, null)
                        Spacer(Modifier.width(6.dp))
                        Text("تکمیل یا ویرایش FFQ")
                    }

                    OutlinedButton(
                        onClick = { onEditRegistration(reg) },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(Icons.Default.Edit, null)
                        Spacer(Modifier.width(6.dp))
                        Text("ویرایش مشخصات")
                    }
                }

                // Excel Export Section (Both Excel Files)
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.4f))
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "خروجی‌های اکسل این پرونده",
                            fontWeight = FontWeight.Bold,
                            fontSize = 15.sp,
                            color = MaterialTheme.colorScheme.secondary
                        )
                        Spacer(Modifier.height(6.dp))
                        Text(
                            text = "ایجاد و مشاهده مستقیم فایل‌های استاندارد اکسل در گوشی یا اشتراک‌گذاری:",
                            fontSize = 12.sp,
                            color = Color.DarkGray
                        )
                        Spacer(Modifier.height(12.dp))

                        // Button 1: Registration & IPAQ Excel
                        Button(
                            onClick = {
                                try {
                                    val file = ExcelExporter.exportRegistrationExcel(
                                        context = context,
                                        records = listOf(currentRecord),
                                        customFileName = "اطلاعات_ثبت_نام_${currentRecord.patientId}.xlsx"
                                    )
                                    Toast.makeText(context, "اکسل مشخصات ایجاد شد", Toast.LENGTH_SHORT).show()
                                    ExcelExporter.openOrShareFile(context, file, "اکسل مشخصات و IPAQ بیمار ${currentRecord.patientId}")
                                } catch (e: Exception) {
                                    Toast.makeText(context, "خطا در خروجی اکسل: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                                }
                            },
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Icon(Icons.Default.TableChart, null)
                            Spacer(Modifier.width(8.dp))
                            Text("خروجی ۱: اکسل اطلاعات ثبت‌نام و IPAQ (۵۲ ستون)")
                        }

                        Spacer(Modifier.height(8.dp))

                        // Button 2: FFQ & 63 Nutrients Excel
                        FilledTonalButton(
                            onClick = {
                                try {
                                    val file = ExcelExporter.exportPatientFFQAndNutrients(
                                        context = context,
                                        record = currentRecord,
                                        allItems = allItems,
                                        customFileName = "بسامد_خوراک_و_مواد_مغذی_${currentRecord.patientId}.xlsx"
                                    )
                                    Toast.makeText(context, "اکسل FFQ و مواد مغذی ایجاد شد", Toast.LENGTH_SHORT).show()
                                    ExcelExporter.openOrShareFile(context, file, "اکسل بسامد خوراک و ۶۳ ماده مغذی بیمار ${currentRecord.patientId}")
                                } catch (e: Exception) {
                                    Toast.makeText(context, "خطا در خروجی اکسل: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                                }
                            },
                            modifier = Modifier.fillMaxWidth(),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Icon(Icons.Default.Description, null)
                            Spacer(Modifier.width(8.dp))
                            Text("خروجی ۲: اکسل بسامد FFQ و تحلیل ۶۳ ماده مغذی")
                        }
                    }
                }

                // Basic Stats Card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.4f))
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("خلاصه وضعیت پرونده", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.height(8.dp))
                        Text("تاریخ ثبت: ${FFQRepository.formatTimestamp(currentRecord.timestamp)}")
                        Text("تعداد اقلام پاسخ‌داده‌شده FFQ: $answeredCount از ۱۴۷")
                        reg.bmi?.let { Text(String.format("شاخص توده بدنی (BMI): %.2f", it), fontWeight = FontWeight.SemiBold) }
                        Text(String.format("نمره فعالیت بدنی (IPAQMET): %.1f", reg.ipaqMet), fontWeight = FontWeight.SemiBold)
                    }
                }

                // Daily Nutrient Intake Preview Card
                if (nutrientTotals.isNotEmpty()) {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                    ) {
                        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text("خلاصه تخمینی دریافت روزانه درشت‌مغذی‌ها و انرژی", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                            Divider(modifier = Modifier.padding(vertical = 4.dp))
                            NutrientRow("انرژی دریافتی کل:", nutrientTotals["kcal"]?.let { String.format("%.0f کیلوکالری", it) } ?: "-")
                            NutrientRow("پروتئین کل:", nutrientTotals["protein(g)"]?.let { String.format("%.1f گرم", it) } ?: "-")
                            NutrientRow("کربوهیدرات کل:", nutrientTotals["cho(g)"]?.let { String.format("%.1f گرم", it) } ?: "-")
                            NutrientRow("چربی کل:", nutrientTotals["fat,total(g)"]?.let { String.format("%.1f گرم", it) } ?: "-")
                            NutrientRow("فیبر کل:", nutrientTotals["fiber,tdr(g)"]?.let { String.format("%.1f گرم", it) } ?: "-")
                            NutrientRow("کلسیم:", nutrientTotals["ca(mg)"]?.let { String.format("%.0f میلی‌گرم", it) } ?: "-")
                            NutrientRow("آهن:", nutrientTotals["fe(mg)"]?.let { String.format("%.1f میلی‌گرم", it) } ?: "-")
                            NutrientRow("ویتامین ث:", nutrientTotals["vit c(mg)"]?.let { String.format("%.1f میلی‌گرم", it) } ?: "-")
                        }
                    }
                }

                // Registration Details Card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("اطلاعات ثبت‌نامی بیمار", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                        Divider(modifier = Modifier.padding(vertical = 4.dp))
                        DetailItem("شناسه (ID):", reg.id)
                        DetailItem("سن:", reg.age)
                        DetailItem("جنسیت:", if (reg.gender == 1) "مرد" else "زن")
                        DetailItem("قد / وزن:", "${reg.heightCm} سانتی‌متر / ${reg.weightKg} کیلوگرم")
                        DetailItem("وضعیت تاهل:", when (reg.marital) { 0 -> "مجرد"; 1 -> "متأهل"; 2 -> "مطلقه"; 3 -> "بیوه"; else -> "نامشخص" })
                        DetailItem("تحصیلات:", when (reg.education) { 0 -> "بی‌سواد/ابتدایی"; 1 -> "راهنمایی/متوسطه"; 2 -> "دیپلم"; 3 -> "لیسانس"; 4 -> "فوق لیسانس و بالاتر"; else -> "نامشخص" })
                        DetailItem("شغل:", when (reg.job) { 0 -> "خانه‌دار"; 1 -> "بازنشسته"; 2 -> "شاغل"; else -> "نامشخص" })
                        DetailItem("تعداد اعضا / فرزندان:", "${reg.familySize} نفر / ${reg.kids} فرزند")
                        DetailItem("سیگار / قلیان / مخدر:", "${reg.cigar.ifBlank { "-" }} / ${reg.ghelian.ifBlank { "-" }} / ${reg.otherNarcotics.ifBlank { "-" }}")
                        DetailItem("دیابت:", when (reg.diabetes) { 1 -> "نوع ۱"; 2 -> "نوع ۲"; 0 -> "خیر"; else -> "-" })
                        DetailItem("فشار خون / بیماری قلبی:", "${if (reg.bp == 1) "بله" else "خیر"} / ${if (reg.cvd == 1) "بله" else "خیر"}")
                    }
                }

                // Answered items preview with notes
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("اقلام ثبت‌شده بسامد خوراک ($answeredCount قلم)", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                        Spacer(Modifier.height(8.dp))
                        if (answeredCount == 0) {
                            Text("هنوز پاسخی برای اقلام FFQ ثبت نشده است.", color = Color.Gray, fontSize = 13.sp)
                        } else {
                            allItems.filter { answers.containsKey(it.id) && !answers[it.id]!!.isEmpty() }.forEach { item ->
                                val ans = answers[item.id]!!
                                val parts = mutableListOf<String>()
                                if (ans.day.isNotBlank()) parts.add("روز: ${ans.day}")
                                if (ans.week.isNotBlank()) parts.add("هفته: ${ans.week}")
                                if (ans.month.isNotBlank()) parts.add("ماه: ${ans.month}")
                                if (ans.year.isNotBlank()) parts.add("سال: ${ans.year}")

                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 4.dp)
                                ) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text("${item.id}. ${item.name}", fontSize = 13.sp, fontWeight = FontWeight.Medium, modifier = Modifier.weight(1f))
                                        Text(parts.joinToString("، "), fontSize = 12.sp, color = MaterialTheme.colorScheme.primary)
                                    }
                                    if (ans.userNotes.isNotBlank()) {
                                        Text(
                                            text = "ملاحظات: ${ans.userNotes}",
                                            fontSize = 11.sp,
                                            color = MaterialTheme.colorScheme.tertiary,
                                            fontWeight = FontWeight.Medium,
                                            modifier = Modifier.padding(top = 2.dp)
                                        )
                                    }
                                }
                                Divider(modifier = Modifier.padding(vertical = 2.dp), color = Color.LightGray.copy(alpha = 0.5f))
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun NutrientRow(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(label, fontSize = 13.sp, color = Color.DarkGray)
        Text(value, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
    }
}

@Composable
fun DetailItem(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(label, fontSize = 13.sp, color = Color.DarkGray)
        Text(value.ifBlank { "-" }, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
    }
}
