<script setup>
import { ListView } from "frappe-ui"
import { createListResource } from 'frappe-ui'
import SideBar from "../component/SideBar.vue"
import { computed } from 'vue'
import Axischart from "../component/Axischart.vue"

const expenses = createListResource({
  doctype: 'Expense',
  fields: ['name', 'expense_date', 'category', 'amount', 'description', 'payment_method'],
  orderBy: 'creation desc',
  auto: true
})

// Corrected computed property
const totalExpense = computed(() => {
  if (!expenses.list.data) return 0
  return expenses.list.data.reduce((sum, item) => sum + Number(item.amount), 0)
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

      <!-- Total Expense Card -->
      <div class="mb-6 p-4 bg-gray-100 rounded-lg shadow w-1/6">
        <span class="font-semibold text-lg">Total Expense:</span>
        <span class="font-bold text-xl text-blue-700"> ${{ totalExpense }}</span>
      </div>

  <div class="flex gap-6">
    <div class="bg-gray shadow-md rounded-lg overflow-auto w-1/2 h-96">
        <ListView
          v-if="expenses.list.data"
          :columns="[
            { label: 'ID', key: 'name'},
            { label: 'Date', key: 'expense_date' },
            { label: 'Category', key: 'category' },
            { label: 'Amount', key: 'amount' },
            { label: 'Payment Method', key: 'payment_method' }
          ]"
          :rows="expenses.list.data"
          :options="{
            showTooltip: false,
            selectable: fasle,
          }"
        />
      </div>
    </div>

    <div class="bg-white shadow-md rounded-lg p-4 w-1/2 h-96">
      <AxisChart/>
    </div>
  </div>
  </div>
  <!-- Expense List -->
  
</template>