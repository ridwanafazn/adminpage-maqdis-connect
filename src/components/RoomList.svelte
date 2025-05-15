<script lang="ts">
  export let rooms = [];
</script>

<ul>
  {#each rooms as room}
    <li>{room.nama_room}</li>
  {/each}
</ul>
