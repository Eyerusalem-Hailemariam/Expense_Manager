<script setup>
import { ListView, Dialog, Button, FormControl, ErrorMessage } from "frappe-ui"
import { createListResource } from "frappe-ui"
import SideBar from "../component/SideBar.vue"
import { computed, reactive, ref } from "vue"
import Axischart from "../component/Axischart.vue"
import ExpenseCard from "../component/ExpenseCard.vue"

const createDialogShown = ref(false)



const expenses = createListResource({
  doctype: "Expense",
  fields: ["name", "expense_date", "category", "amount", "description", "payment_method"],
  orderBy: "creation desc",
  auto: true
})

const totalExpense = computed(() => {
  if (!expenses.list || !expenses.list.data) return 0
  return expenses.list.data.reduce((sum, item) => sum + Number(item.amount), 0)
})

const chartConfig = computed(() => {
  const monthlyTotals = {}
  if (expenses.list && expenses.list.data) {
    expenses.list.data.forEach(item => {
      const date = new Date(item.expense_date)
      const month = date.toLocaleString("default", { month: "short" })
      monthlyTotals[month] = (monthlyTotals[month] || 0) + Number(item.amount)
    })
  }

  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
  const data = months.map(m => ({ month: m, expenses: monthlyTotals[m] || 0 }))

  return {
    data,
    title: "Monthly Expense",
    colors: ["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6"], 
    xAxis: { key: "month", type: "category", title: 'Month', timeGrain: 'month' },
    yAxis: { 
      title: "Amount ($)", 
      echartOptions: { min: 0, max: Math.max(...data.map(d => d.expenses)) || 0 }
    },
    series: [{ 
      name: "expenses", type: "bar", value: "expenses",
      legend: { show: true, position: "top" }
    }],
  }
})
</script>

<template>
<div class="flex h-screen bg-white-100 text-gray-800">
  <!-- Sidebar -->
  <div class="w-64 bg-white shadow-lg">
    <SideBar />
  </div>

  <!-- Main content -->
  <div class="flex-1 p-6 overflow-auto">
    <h1 class="text-2xl font-bold mb-6 text-black-700">Expense Dashboard</h1>

<div class="flex items-center justify-between mb-6">
  <h2 class="text-lg font-semibold">
    Total Expense: <span class="text-xl font-bold text-blue-700">${{ totalExpense }}</span>
  </h2>
  <ExpenseCard :expenses="expenses" />
</div>


    <div class="flex gap-6 items-center mt-20">
      <!-- ListView -->
      <div class="bg-gray shadow-md rounded-lg overflow-auto w-1/2 h-80 mb-40">
        <ListView
          v-if="expenses.list"
          rowKey="name"
          :columns="[
            { label: 'ID', key: 'name' },
            { label: 'Date', key: 'expense_date' },
            { label: 'Category', key: 'category' },
            { label: 'Amount', key: 'amount' },
            { label: 'Payment Method', key: 'payment_method' }
          ]"
          :rows="expenses.list.data"
          :options="{ showTooltip: false, selectable: false }"
        />
      </div>

     
      <!-- Chart -->
      <div class="bg-white shadow-md rounded-lg p-4 w-1/2 h-80 mb-40 flex items-center justify-center">
        <Axischart :chartConfig="chartConfig" />
      </div>
    </div>
  </div>
</div>
</template>