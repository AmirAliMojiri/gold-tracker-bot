package com.users.ffq_app.util

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Environment
import android.widget.Toast
import androidx.core.content.FileProvider
import com.users.ffq_app.data.model.FFQItem
import com.users.ffq_app.data.model.PatientRecord
import java.io.File
import java.io.FileOutputStream
import java.nio.charset.StandardCharsets
import java.util.zip.ZipEntry
import java.util.zip.ZipOutputStream

data class XlsxCell(
    val value: Any?,
    val isHeader: Boolean = false
)

data class XlsxSheet(
    val title: String,
    val rows: List<List<XlsxCell>>
)

object ExcelExporter {

    private fun escapeXml(str: String): String {
        return str.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&apos;")
    }

    private fun getColName(colIdx: Int): String {
        var col = colIdx
        val sb = StringBuilder()
        while (col > 0) {
            val rem = (col - 1) % 26
            sb.append(('A'.code + rem).toChar())
            col = (col - 1) / 26
        }
        return sb.reverse().toString()
    }

    fun buildXlsxFile(sheets: List<XlsxSheet>, outputFile: File) {
        outputFile.parentFile?.mkdirs()
        ZipOutputStream(FileOutputStream(outputFile)).use { zos ->
            // 1. [Content_Types].xml
            val contentTypesSb = StringBuilder()
            contentTypesSb.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
            contentTypesSb.append("<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">\n")
            contentTypesSb.append("  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>\n")
            contentTypesSb.append("  <Default Extension=\"xml\" ContentType=\"application/xml\"/>\n")
            contentTypesSb.append("  <Override PartName=\"/xl/workbook.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>\n")
            contentTypesSb.append("  <Override PartName=\"/xl/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml\"/>\n")
            for (i in sheets.indices) {
                contentTypesSb.append("  <Override PartName=\"/xl/worksheets/sheet${i + 1}.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>\n")
            }
            contentTypesSb.append("</Types>")
            writeZipEntry(zos, "[Content_Types].xml", contentTypesSb.toString())

            // 2. _rels/.rels
            val rootRels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" +
                    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n" +
                    "  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"xl/workbook.xml\"/>\n" +
                    "</Relationships>"
            writeZipEntry(zos, "_rels/.rels", rootRels)

            // 3. xl/_rels/workbook.xml.rels
            val wbRelsSb = StringBuilder()
            wbRelsSb.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
            wbRelsSb.append("<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n")
            for (i in sheets.indices) {
                wbRelsSb.append("  <Relationship Id=\"rId${i + 1}\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet${i + 1}.xml\"/>\n")
            }
            wbRelsSb.append("  <Relationship Id=\"rId${sheets.size + 1}\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" Target=\"styles.xml\"/>\n")
            wbRelsSb.append("</Relationships>")
            writeZipEntry(zos, "xl/_rels/workbook.xml.rels", wbRelsSb.toString())

            // 4. xl/workbook.xml
            val wbSb = StringBuilder()
            wbSb.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
            wbSb.append("<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">\n")
            wbSb.append("  <sheets>\n")
            for (i in sheets.indices) {
                wbSb.append("    <sheet name=\"${escapeXml(sheets[i].title)}\" sheetId=\"${i + 1}\" r:id=\"rId${i + 1}\"/>\n")
            }
            wbSb.append("  </sheets>\n")
            wbSb.append("</workbook>")
            writeZipEntry(zos, "xl/workbook.xml", wbSb.toString())

            // 5. xl/styles.xml
            val stylesXml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" +
                    "<styleSheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">\n" +
                    "  <fonts count=\"2\">\n" +
                    "    <font><name val=\"Calibri\"/><sz val=\"11\"/></font>\n" +
                    "    <font><b/><name val=\"Calibri\"/><sz val=\"11\"/><color rgb=\"FFFFFFFF\"/></font>\n" +
                    "  </fonts>\n" +
                    "  <fills count=\"3\">\n" +
                    "    <fill><patternFill patternType=\"none\"/></fill>\n" +
                    "    <fill><patternFill patternType=\"gray125\"/></fill>\n" +
                    "    <fill><patternFill patternType=\"solid\"><fgColor rgb=\"FF1F4E79\"/><bgColor indexed=\"64\"/></patternFill></fill>\n" +
                    "  </fills>\n" +
                    "  <borders count=\"1\">\n" +
                    "    <border><left/><right/><top/><bottom/><diagonal/></border>\n" +
                    "  </borders>\n" +
                    "  <cellStyleXfs count=\"1\">\n" +
                    "    <xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\"/>\n" +
                    "  </cellStyleXfs>\n" +
                    "  <cellXfs count=\"2\">\n" +
                    "    <xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\" xfId=\"0\"/>\n" +
                    "    <xf numFmtId=\"0\" fontId=\"1\" fillId=\"2\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyFill=\"1\" applyAlignment=\"1\">\n" +
                    "      <alignment horizontal=\"center\" vertical=\"center\"/>\n" +
                    "    </xf>\n" +
                    "  </cellXfs>\n" +
                    "  <cellStyles count=\"1\">\n" +
                    "    <cellStyle name=\"Normal\" xfId=\"0\" builtinId=\"0\"/>\n" +
                    "  </cellStyles>\n" +
                    "</styleSheet>"
            writeZipEntry(zos, "xl/styles.xml", stylesXml)

            // 6. Each Sheet
            for (i in sheets.indices) {
                val sheet = sheets[i]
                val sheetSb = StringBuilder()
                sheetSb.append("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
                sheetSb.append("<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">\n")
                sheetSb.append("  <sheetViews><sheetView rightToLeft=\"1\" workbookViewId=\"0\"/></sheetViews>\n")
                sheetSb.append("  <sheetData>\n")

                for (rIdx in sheet.rows.indices) {
                    val rowNum = rIdx + 1
                    val row = sheet.rows[rIdx]
                    sheetSb.append("    <row r=\"$rowNum\">\n")
                    for (cIdx in row.indices) {
                        val cellRef = "${getColName(cIdx + 1)}$rowNum"
                        val cell = row[cIdx]
                        val sAttr = if (cell.isHeader) " s=\"1\"" else ""
                        val v = cell.value

                        if (v == null || (v is String && v.isBlank())) {
                            if (cell.isHeader) {
                                sheetSb.append("      <c r=\"$cellRef\"$sAttr t=\"inlineStr\"><is><t></t></is></c>\n")
                            }
                        } else if (v is Number && !cell.isHeader) {
                            sheetSb.append("      <c r=\"$cellRef\"$sAttr><v>$v</v></c>\n")
                        } else {
                            val text = escapeXml(v.toString())
                            sheetSb.append("      <c r=\"$cellRef\"$sAttr t=\"inlineStr\"><is><t>$text</t></is></c>\n")
                        }
                    }
                    sheetSb.append("    </row>\n")
                }

                sheetSb.append("  </sheetData>\n")
                sheetSb.append("</worksheet>")
                writeZipEntry(zos, "xl/worksheets/sheet${i + 1}.xml", sheetSb.toString())
            }
        }
    }

    private fun writeZipEntry(zos: ZipOutputStream, entryName: String, content: String) {
        val entry = ZipEntry(entryName)
        zos.putNextEntry(entry)
        val bytes = content.toByteArray(StandardCharsets.UTF_8)
        zos.write(bytes, 0, bytes.size)
        zos.closeEntry()
    }

    // --- 1. Export Registration Data (AutomatedDataMain_2.xlsx format) ---
    fun exportRegistrationExcel(
        context: Context,
        records: List<PatientRecord>,
        customFileName: String = "اطلاعات_ثبت_نام_بیماران.xlsx"
    ): File {
        val headers = listOf(
            "ID", "DiagnosisMO", "Marital", "other Narcotics", "ghelian", "Cigar", "Aspirin", "Levotyroxin",
            "Statin", "VitD", "Multivitamin", "Diabetes", "CVD", "BP", "Migrane", "GID", "Cancer",
            "WeightKg", "HeightCm", "BMI", "Gender", "Age", "Education", "Job", "FamilySize", "Kids", "HouseOwnership",
            "IPAQ2", "IPAQ3", "IPAQ4", "IPAQ5", "IPAQ6", "IPAQ7", "IPAQ8", "IPAQ9", "IPAQ10", "IPAQ11",
            "IPAQ12", "IPAQ13", "IPAQ14", "IPAQ15", "IPAQ16", "IPAQ17", "IPAQ18", "IPAQ19", "IPAQ20",
            "IPAQ21", "IPAQ22", "IPAQ23", "IPAQ24", "IPAQ25", "IPAQMET"
        )

        val headerRow = headers.map { XlsxCell(it, isHeader = true) }
        val allRows = mutableListOf(headerRow)

        for (record in records) {
            val reg = record.registration
            val row = mutableListOf<XlsxCell>()
            row.add(XlsxCell(reg.id.ifBlank { record.patientId }))
            row.add(XlsxCell(reg.diagnosisMO))
            row.add(XlsxCell(reg.marital ?: ""))
            row.add(XlsxCell(reg.otherNarcotics))
            row.add(XlsxCell(reg.ghelian))
            row.add(XlsxCell(reg.cigar))
            row.add(XlsxCell(reg.aspirin ?: ""))
            row.add(XlsxCell(reg.levotyroxin ?: ""))
            row.add(XlsxCell(reg.statin))
            row.add(XlsxCell(reg.vitD ?: ""))
            row.add(XlsxCell(reg.multivitamin ?: ""))
            row.add(XlsxCell(reg.diabetes ?: ""))
            row.add(XlsxCell(reg.cvd ?: ""))
            row.add(XlsxCell(reg.bp ?: ""))
            row.add(XlsxCell(reg.migrane ?: ""))
            row.add(XlsxCell(reg.gid ?: ""))
            row.add(XlsxCell(reg.cancer ?: ""))
            row.add(XlsxCell(reg.weightKg.toDoubleOrNull() ?: reg.weightKg))
            row.add(XlsxCell(reg.heightCm.toDoubleOrNull() ?: reg.heightCm))
            row.add(XlsxCell(reg.bmi?.let { Math.round(it * 100.0) / 100.0 } ?: ""))
            row.add(XlsxCell(reg.gender ?: ""))
            row.add(XlsxCell(reg.age.toIntOrNull() ?: reg.age))
            row.add(XlsxCell(reg.education ?: ""))
            row.add(XlsxCell(reg.job ?: ""))
            row.add(XlsxCell(reg.familySize.toIntOrNull() ?: reg.familySize))
            row.add(XlsxCell(reg.kids.toIntOrNull() ?: reg.kids))
            row.add(XlsxCell(reg.houseOwnership ?: ""))

            // IPAQ 2 to 25
            for (p in 2..25) {
                val ipaqVal = reg.ipaq[p] ?: ""
                row.add(XlsxCell(ipaqVal.toDoubleOrNull() ?: ipaqVal))
            }
            row.add(XlsxCell(Math.round(reg.ipaqMet * 10.0) / 10.0))

            allRows.add(row)
        }

        val sheet = XlsxSheet("Registration_IPAQ", allRows)
        val file = getExportFile(context, customFileName)
        buildXlsxFile(listOf(sheet), file)
        copyToPublicDownloads(file)
        return file
    }

    // --- 2. Export FFQ Questionnaire & 63 Nutrients Analysis ---
    fun exportPatientFFQAndNutrients(
        context: Context,
        record: PatientRecord,
        allItems: List<FFQItem>,
        customFileName: String = "بسامد_خوراک_و_مواد_مغذی_${record.patientId}.xlsx"
    ): File {
        // Sheet 1: FFQ Items & Answers
        val ffqHeaders = listOf(
            "ردیف", "نام ماده غذایی", "اندازه سهم", "روز", "هفته", "ماه", "سال",
            "معادل مصرف روزانه", "ملاحظات"
        )
        val ffqHeaderRow = ffqHeaders.map { XlsxCell(it, isHeader = true) }
        val ffqRows = mutableListOf(ffqHeaderRow)

        // Calculate nutrient totals
        val nutrientTotals = mutableMapOf<String, Double>()

        for (item in allItems) {
            val ans = record.answers[item.id]
            val mult = ans?.toDailyMultiplier() ?: 0.0

            if (mult > 0) {
                for ((nutKey, factor) in item.nutrients) {
                    nutrientTotals[nutKey] = (nutrientTotals[nutKey] ?: 0.0) + (mult * factor)
                }
            }

            val noteStr = ans?.userNotes?.ifBlank { item.notes } ?: item.notes

            ffqRows.add(
                listOf(
                    XlsxCell(item.id),
                    XlsxCell(item.name),
                    XlsxCell(item.portion),
                    XlsxCell(ans?.day ?: ""),
                    XlsxCell(ans?.week ?: ""),
                    XlsxCell(ans?.month ?: ""),
                    XlsxCell(ans?.year ?: ""),
                    XlsxCell(if (mult > 0) Math.round(mult * 100.0) / 100.0 else ""),
                    XlsxCell(noteStr)
                )
            )
        }

        // Sheet 2: 63 Nutrients Daily Intake Summary
        val nutHeaders = listOf("ردیف", "نام ماده مغذی", "واحد اندازه‌گیری", "مجموع دریافتی روزانه بیمار", "منبع داده")
        val nutHeaderRow = nutHeaders.map { XlsxCell(it, isHeader = true) }
        val nutRows = mutableListOf(nutHeaderRow)

        val sampleItem = allItems.firstOrNull { it.nutrients.isNotEmpty() }
        val nutrientKeys = sampleItem?.nutrients?.keys?.toList() ?: emptyList()

        for (idx in nutrientKeys.indices) {
            val nutName = nutrientKeys[idx]
            var unit = ""
            if (nutName.contains("(") && nutName.contains(")")) {
                unit = nutName.substring(nutName.indexOf("(") + 1, nutName.indexOf(")"))
            }
            val intake = nutrientTotals[nutName] ?: 0.0
            nutRows.add(
                listOf(
                    XlsxCell(idx + 1),
                    XlsxCell(nutName),
                    XlsxCell(unit),
                    XlsxCell(Math.round(intake * 100.0) / 100.0),
                    XlsxCell("محاسبه شده از جداول Nutrients Forme")
                )
            )
        }

        val sheet1 = XlsxSheet("بسامد_خوراک_FFQ", ffqRows)
        val sheet2 = XlsxSheet("تحلیل_مواد_مغذی", nutRows)

        val file = getExportFile(context, customFileName)
        buildXlsxFile(listOf(sheet1, sheet2), file)
        copyToPublicDownloads(file)
        return file
    }

    // --- 3. Export Multi-Patient Nutrients Summary ---
    fun exportAllPatientsNutrientSummary(
        context: Context,
        records: List<PatientRecord>,
        allItems: List<FFQItem>,
        customFileName: String = "خلاصه_مواد_مغذی_کلیه_بیماران.xlsx"
    ): File {
        val sampleItem = allItems.firstOrNull { it.nutrients.isNotEmpty() }
        val nutrientKeys = sampleItem?.nutrients?.keys?.toList() ?: emptyList()

        val headers = mutableListOf("ردیف", "شناسه بیمار", "سن", "جنسیت", "BMI", "IPAQMET")
        headers.addAll(nutrientKeys)

        val headerRow = headers.map { XlsxCell(it, isHeader = true) }
        val rows = mutableListOf(headerRow)

        for (rIdx in records.indices) {
            val record = records[rIdx]
            val reg = record.registration

            // Calc nutrients
            val patientTotals = mutableMapOf<String, Double>()
            for (item in allItems) {
                val ans = record.answers[item.id] ?: continue
                val mult = ans.toDailyMultiplier()
                if (mult <= 0) continue
                for ((nutKey, factor) in item.nutrients) {
                    patientTotals[nutKey] = (patientTotals[nutKey] ?: 0.0) + (mult * factor)
                }
            }

            val row = mutableListOf<XlsxCell>()
            row.add(XlsxCell(rIdx + 1))
            row.add(XlsxCell(record.patientId))
            row.add(XlsxCell(reg.age.toIntOrNull() ?: reg.age))
            row.add(XlsxCell(if (reg.gender == 1) "مرد" else if (reg.gender == 0) "زن" else ""))
            row.add(XlsxCell(reg.bmi?.let { Math.round(it * 100.0) / 100.0 } ?: ""))
            row.add(XlsxCell(Math.round(reg.ipaqMet * 10.0) / 10.0))

            for (nut in nutrientKeys) {
                val intake = patientTotals[nut] ?: 0.0
                row.add(XlsxCell(Math.round(intake * 100.0) / 100.0))
            }
            rows.add(row)
        }

        val sheet = XlsxSheet("خلاصه_تغذیه_بیماران", rows)
        val file = getExportFile(context, customFileName)
        buildXlsxFile(listOf(sheet), file)
        copyToPublicDownloads(file)
        return file
    }

    private fun getExportFile(context: Context, fileName: String): File {
        val docsDir = context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS) ?: context.filesDir
        val exportDir = File(docsDir, "FFQ_Exports")
        exportDir.mkdirs()
        return File(exportDir, fileName)
    }

    private fun copyToPublicDownloads(file: File) {
        try {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            val appDir = File(downloadsDir, "FFQ_Reports")
            appDir.mkdirs()
            val dest = File(appDir, file.name)
            file.inputStream().use { input ->
                dest.outputStream().use { output ->
                    input.copyTo(output)
                }
            }
        } catch (_: Exception) {}
    }

    fun openOrShareFile(context: Context, file: File, title: String = "مشاهده فایل اکسل") {
        try {
            val uri: Uri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.provider",
                file
            )

            val viewIntent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }

            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                putExtra(Intent.EXTRA_STREAM, uri)
                putExtra(Intent.EXTRA_SUBJECT, title)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }

            val chooser = Intent.createChooser(shareIntent, title).apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }

            try {
                context.startActivity(viewIntent)
            } catch (e: Exception) {
                context.startActivity(chooser)
            }
        } catch (e: Exception) {
            Toast.makeText(context, "خطا در باز کردن فایل: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
        }
    }
}
