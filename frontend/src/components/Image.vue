<template>
  <img
    :src="require(`@/img/${name}.png`)"
    :class="$attrs.class || 'w-20 h-20'"
  />
</template>
<script>
export default {
  props: ["name"],
};
</script>
