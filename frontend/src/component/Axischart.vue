//componet/Axischart

<script setup>
import { AxisChart } from "frappe-ui"

const props = defineProps({
  chartConfig: {
    type: Object,
    required: true
  }
})

</script>

<template>
  <div class="w-full h-200">
    <AxisChart v-if="chartConfig.data.length" :key="JSON.stringify(chartConfig.data)" :config="chartConfig" />
  </div>
</template>