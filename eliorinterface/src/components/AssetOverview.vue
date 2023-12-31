

<template>
  <div>
    <h2>Asset Overview</h2>
    <ul>
      <li v-for="asset in assets" :key="asset.asset_name">
        {{ asset.asset_name }} - {{ asset.ip_addr }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AssetOverview',
  props: {
    assets: Array,
  },
};
</script>
