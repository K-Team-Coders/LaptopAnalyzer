<template>
  <div
    :style="rectangleStyle"
    class="absolute border-2 border-red-500 bg-transparent cursor-move"
    @mousedown="startDrag"
  >
    <div class="absolute top-0 left-0 w-full h-full">
      <input
        v-model="this.localName"
        class="absolute bg-white border border-gray-300 rounded px-1 py-0.5 text-xs"
        :style="nameInputStyle"
        @blur="emitUpdate"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    coords: {
      type: Array,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      localCoords: [...this.coords],
      localName: this.name,
      dragging: false,
      startX: 0,
      startY: 0,
    };
  },
  computed: {
    rectangleStyle() {
      const [x, y, width, height] = this.localCoords;
      return {
        left: `${x}px`,
        top: `${y}px`,
        width: `${width}px`,
        height: `${height}px`,
      };
    },
    nameInputStyle() {
      return {
        top: "-20px",
        left: "5px",
      };
    },
  },
  methods: {
    startDrag(event) {
      event.preventDefault();
      this.dragging = true;
      this.startX = event.clientX - this.localCoords[0];
      this.startY = event.clientY - this.localCoords[1];
      document.addEventListener("mousemove", this.onMouseMove);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onMouseMove(event) {
      if (!this.dragging) return;
      const x = event.clientX - this.startX;
      const y = event.clientY - this.startY;
      this.localCoords[0] = x;
      this.localCoords[1] = y;
      this.emitUpdate();
    },
    stopDrag() {
      this.dragging = false;
      document.removeEventListener("mousemove", this.onMouseMove);
      document.removeEventListener("mouseup", this.stopDrag);
    },

    emitUpdate() {
      this.$emit("update-defect", {
        coords: [...this.localCoords],
        name: this.localName,
      });
    },
  },
  watch: {
    coords(newCoords) {
      this.localCoords = [...newCoords];
    },
    name(newName) {
      this.localName = newName;
    },
  },
};
</script>

<style>
.absolute {
  position: absolute;
}
.cursor-move {
  cursor: move;
}
</style>
