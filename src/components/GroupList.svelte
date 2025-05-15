<script lang="ts">
  export let groups = [];
</script>

<ul>
  {#each groups as group}
    <li>{group.nama_grup}</li>
  {/each}
</ul>
