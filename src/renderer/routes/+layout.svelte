<script lang="ts">
    // @ts-nocheck
    export let params = {};
    import { pixelExplosion } from '$lib/mouseEffects';
</script>

<div use:pixelExplosion style="height: 100vh; width: 100vw;">
    <slot />
</div> 