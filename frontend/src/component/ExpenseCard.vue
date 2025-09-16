<script setup>
import { Dialog, FormControl, ErrorMessage } from "frappe-ui"
import { reactive, ref } from "vue"

const props = defineProps({
  expenses: Object   // get expenses resource from parent
})

const createDialogShown = ref(false)

const newExpense = reactive({
  expense_date: '',
  category: '',
  amount: '',
  payment_method: '',
  description: '',
})

const categories = [
  { label: "Travel", value: "Travel" },
  { label: "Food", value: "Food" },
  { label: "Office Supplies", value: "Office-Supplies" }
]

const payments = [
  { label: "Cash", value: "Cash" },
  { label: "Card", value: "Card" },
  { label: "Bank Transfer", value: "Bank-transfer" }
]
</script>

<template>

  <Button variant="solid" @click="createDialogShown = true">Create</Button>

  <!-- Dialog -->
  <Dialog :options="{
    title: 'New Expense',
    size: 'xl',
    actions: [
      {
        label: 'Create',
        variant: 'solid',
        onClick(close) {
          props.expenses.insert.submit({ ...newExpense }, { onSuccess() { close() } })
        }
      }
    ]
  }" v-model="createDialogShown">
    <template #body-content>
      <form class="space-y-3">
        <FormControl type="date" label="Expense Date" v-model="newExpense.expense_date" required />
        <FormControl type="number" label="Amount" v-model="newExpense.amount" required />
        <FormControl type="select" label="Category" v-model="newExpense.category"
          :options="categories" :hideSearch="false" :selectable="true" required />
        <FormControl type="select" label="Payment Method" v-model="newExpense.payment_method"
          :options="payments" placeholder="Select Payment" :hideSearch="false" :selectable="true" required />
        <FormControl label="Description" v-model="newExpense.description"
          placeholder="Add a note (optional)" type="textarea" />
      </form>
      <ErrorMessage class="mt-2" :message="props.expenses.insert.error" />
    </template>
  </Dialog>
</template>