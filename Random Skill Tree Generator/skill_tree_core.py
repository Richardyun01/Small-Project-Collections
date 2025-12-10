import random
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


NodeId = Tuple[int, int]  # (level, index)
Edge = Tuple[NodeId, NodeId]  # ((L1, i1), (L2, i2))


@dataclass
class TreeConfig:
    start_count: int
    end_count: int
    height: int
    max_width: int
    extra_edge_prob: float = 0.3
    max_index_diff: Optional[int] = None  # None이면 인덱스 거리 제약 없음


class SkillTree:
    """트리의 레벨/간선 데이터와 생성 규칙을 캡슐화."""

    def __init__(self, config: TreeConfig) -> None:
        self.config = config
        self.levels: List[List[str]] = []
        self.edges: List[Edge] = []

    # --------- 외부에 노출되는 메인 메서드 --------- #
    def generate(self) -> None:
        self.levels = self._generate_levels()
        self.edges = self._generate_random_edges()

    # --------- 내부: 레벨 생성 --------- #
    def _generate_levels(self) -> List[List[str]]:
        c = self.config

        if c.start_count < 1:
            raise ValueError("Starting count too small. Minimum is 1.")
        if c.start_count > c.max_width:
            raise ValueError("Starting count cannot be larger than max width.")
        if c.end_count < 1:
            raise ValueError("Ending count too small. Minimum is 1.")
        if c.end_count > c.max_width:
            raise ValueError("Ending count cannot be larger than max width.")
        if c.height < 2:
            raise ValueError("Height too small. Minimum is 2.")
        if c.height > 30:
            raise ValueError("Height too large. Maximum is 30.")
        if c.max_width < 1:
            raise ValueError("Width too small. Minimum is 1.")
        if c.max_width > 30:
            raise ValueError("Width too large. Maximum is 30.")

        levels: List[List[str]] = []
        # 첫 레벨
        levels.append([f"L0_N{i}" for i in range(c.start_count)])

        # 중간 레벨
        for h in range(1, c.height - 1):
            count = random.randint(1, c.max_width)
            levels.append([f"L{h}_N{i}" for i in range(count)])

        # 마지막 레벨
        levels.append([f"L{c.height - 1}_N{i}" for i in range(c.end_count)])
        return levels

    # --------- 내부: 간선 생성 --------- #
    def _generate_random_edges(self) -> List[Edge]:
        if not self.levels:
            raise RuntimeError("Levels are empty. Call generate() first.")

        levels = self.levels
        extra_edge_prob = self.config.extra_edge_prob
        max_index_diff = self.config.max_index_diff

        height = len(levels)
        parent_count: Dict[NodeId, int] = {}
        child_count: Dict[NodeId, int] = {}

        for L, nodes in enumerate(levels):
            for i in range(len(nodes)):
                parent_count[(L, i)] = 0
                child_count[(L, i)] = 0

        edges: List[Edge] = []

        for L in range(height - 1):
            num_parents = len(levels[L])
            num_children = len(levels[L + 1])

            # 각 부모가 최소 1개의 자식
            for i in range(num_parents):
                if max_index_diff is not None:
                    candidate_children = [
                        j for j in range(num_children) if abs(i - j) <= max_index_diff
                    ]
                else:
                    candidate_children = list(range(num_children))

                # 제약 때문에 후보가 없으면 전체 자식 중 랜덤
                if not candidate_children:
                    candidate_children = list(range(num_children))

                j = random.choice(candidate_children)
                edge = ((L, i), (L + 1, j))
                edges.append(edge)
                parent_count[(L + 1, j)] += 1
                child_count[(L, i)] += 1

            # 각 자식이 최소 1개의 부모
            for j in range(num_children):
                if parent_count[(L + 1, j)] == 0:
                    if max_index_diff is not None:
                        candidate_parents = [
                            i
                            for i in range(num_parents)
                            if abs(i - j) <= max_index_diff
                        ]
                    else:
                        candidate_parents = list(range(num_parents))

                    # 제약으로 후보가 0개면 전체 부모에서 선택
                    if not candidate_parents:
                        candidate_parents = list(range(num_parents))

                    i = random.choice(candidate_parents)
                    edge = ((L, i), (L + 1, j))
                    edges.append(edge)
                    parent_count[(L + 1, j)] += 1
                    child_count[(L, i)] += 1

            # 추가 랜덤 간선
            for i in range(num_parents):
                for j in range(num_children):
                    if max_index_diff is not None and abs(i - j) > max_index_diff:
                        continue

                    if random.random() < extra_edge_prob:
                        candidate = ((L, i), (L + 1, j))
                        if candidate not in edges:
                            edges.append(candidate)
                            parent_count[(L + 1, j)] += 1
                            child_count[(L, i)] += 1

        return edges


# --------- 위치 계산 + 렌더링 --------- #
def _compute_positions(
    levels: List[List[str]],
    node_size: float = 0.6,
    h_gap: float = 1.8,
    v_gap: float = 2.0,
    level_gaps=None,
    orientation: str = "top_down",
) -> Dict[NodeId, Tuple[float, float]]:
    positions: Dict[NodeId, Tuple[float, float]] = {}

    if level_gaps is not None:
        gaps = level_gaps
    else:
        gaps = [v_gap] * (len(levels) - 1)

    if orientation in ("top_down", "bottom_up"):
        y_levels = [0.0]
        for g in gaps:
            if orientation == "top_down":
                y_levels.append(y_levels[-1] - g)
            else:
                y_levels.append(y_levels[-1] + g)

        for L, level_nodes in enumerate(levels):
            n = len(level_nodes)
            y = y_levels[L]
            for i in range(n):
                x = (i - (n - 1) / 2) * h_gap
                positions[(L, i)] = (x, y)

    elif orientation == "left_right":
        x_levels = [0.0]
        for g in gaps:
            x_levels.append(x_levels[-1] + g)

        for L, level_nodes in enumerate(levels):
            n = len(level_nodes)
            x = x_levels[L]
            for i in range(n):
                y = (i - (n - 1) / 2) * h_gap
                positions[(L, i)] = (x, y)
    else:
        raise ValueError(f"Unknown orientation: {orientation}")

    return positions


class SkillTreeRenderer:
    """SkillTree 객체를 matplotlib Figure로 그리는 책임만 담당."""

    def create_figure(
        self,
        tree: SkillTree,
        orientation: str = "top_down",
        fig_width: Optional[float] = None,
        fig_height: Optional[float] = None,
    ):
        levels = tree.levels
        edges = tree.edges

        if not levels or not edges:
            raise RuntimeError("Tree is empty. Generate it before rendering.")

        num_layers = len(levels)
        max_width = max(len(lvl) for lvl in levels) if levels else 1

        complexity = max(num_layers, max_width)
        spacing_scale = 1.0 + 0.25 * max(complexity - 4, 0)
        spacing_scale = min(spacing_scale, 4.0)

        base_node_size = 1.3
        node_size = base_node_size * min(spacing_scale, 3)

        base_fontsize = 8
        fontsize = max(4, int(base_fontsize / spacing_scale))

        base_h_gap = 1.8
        base_v_gap = 3.0
        h_gap = base_h_gap * spacing_scale

        base_gap = base_v_gap * spacing_scale
        edge_factor = 0.05 * spacing_scale
        max_gap = 5.0 * spacing_scale

        # 레벨 별 간선 수
        edges_by_layer_count = {(L, L + 1): 0 for L in range(num_layers - 1)}
        for (L1, _i1), (L2, _i2) in edges:
            if L2 == L1 + 1:
                edges_by_layer_count[(L1, L2)] += 1

        level_gaps = []
        for L in range(num_layers - 1):
            ecount = edges_by_layer_count.get((L, L + 1), 0)
            gap = base_gap + edge_factor * ecount
            gap = min(gap, max_gap)
            level_gaps.append(gap)

        positions = _compute_positions(
            levels,
            node_size=node_size,
            h_gap=h_gap,
            level_gaps=level_gaps,
            orientation=orientation,
        )

        all_x = [pos[0] for pos in positions.values()]
        all_y = [pos[1] for pos in positions.values()]

        span_x = max(all_x) - min(all_x) if all_x else 1.0
        span_y = max(all_y) - min(all_y) if all_y else 1.0

        fig_scale = 0.7 * (spacing_scale**0.5)

        min_w, min_h = 6.0, 4.0
        max_w, max_h = 30.0, 20.0

        auto_fig_w = max(min_w, min(max_w, span_x * fig_scale))
        auto_fig_h = max(min_h, min(max_h, span_y * fig_scale))

        if fig_width is not None and fig_height is not None:
            fig_w, fig_h = fig_width, fig_height
        else:
            fig_w, fig_h = auto_fig_w, auto_fig_h

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        # 노드
        for (L, i), (x, y) in positions.items():
            rect = Rectangle(
                (x - node_size / 2, y - node_size / 2),
                node_size,
                node_size,
                fill=True,
                edgecolor="black",
                linewidth=1.2,
            )
            ax.add_patch(rect)
            ax.text(
                x,
                y,
                f"{L},{i}",
                ha="center",
                va="center",
                fontsize=fontsize,
            )

        # 간선 그룹화
        edges_group = {}
        for (L1, i1), (L2, i2) in edges:
            key = (L1, L2)
            edges_group.setdefault(key, []).append(((L1, i1), (L2, i2)))

        # 간선 그리기
        if orientation in ("top_down", "bottom_up"):
            vertical_spacing = 0.25 * spacing_scale
            margin_y = 0.05 * spacing_scale

            for (L1, L2), edge_list in edges_group.items():
                m = len(edge_list)
                for k, ((pL, pi), (cL, ci)) in enumerate(edge_list):
                    x1, y1 = positions[(pL, pi)]
                    x2, y2 = positions[(cL, ci)]

                    y_low, y_high = sorted([y1, y2])
                    lower_rect_top = y_low + node_size / 2
                    upper_rect_bottom = y_high - node_size / 2

                    safe_min_y = lower_rect_top + margin_y
                    safe_max_y = upper_rect_bottom - margin_y

                    if safe_min_y >= safe_max_y:
                        safe_mid = (lower_rect_top + upper_rect_bottom) / 2.0
                        safe_min_y = safe_mid
                        safe_max_y = safe_mid

                    base_mid_y = (y1 + y2) / 2.0
                    offset = (k - (m - 1) / 2) * vertical_spacing
                    mid_y = base_mid_y + offset

                    if mid_y < safe_min_y:
                        mid_y = safe_min_y
                    elif mid_y > safe_max_y:
                        mid_y = safe_max_y

                    if y2 < y1:
                        y_start = y1 - node_size / 2
                        y_end = y2 + node_size / 2
                    else:
                        y_start = y1 + node_size / 2
                        y_end = y2 - node_size / 2

                    x_start = x1
                    x_end = x2

                    x_mid1, y_mid1 = x1, mid_y
                    x_mid2, y_mid2 = x2, mid_y

                    ax.plot([x_start, x_mid1], [y_start, y_mid1], linewidth=0.8)
                    ax.plot([x_mid1, x_mid2], [y_mid1, y_mid2], linewidth=0.8)
                    ax.plot([x_mid2, x_end], [y_mid2, y_end], linewidth=0.8)

        elif orientation == "left_right":
            horizontal_spacing = 0.25 * spacing_scale
            margin_x = 0.05 * spacing_scale

            for (L1, L2), edge_list in edges_group.items():
                m = len(edge_list)
                for k, ((pL, pi), (cL, ci)) in enumerate(edge_list):
                    x1, y1 = positions[(pL, pi)]
                    x2, y2 = positions[(cL, ci)]

                    parent_right = x1 + node_size / 2
                    child_left = x2 - node_size / 2

                    safe_min_x = parent_right + margin_x
                    safe_max_x = child_left - margin_x

                    if safe_min_x >= safe_max_x:
                        safe_mid = (parent_right + child_left) / 2.0
                        safe_min_x = safe_mid
                        safe_max_x = safe_mid

                    base_mid_x = (x1 + x2) / 2.0
                    offset = (k - (m - 1) / 2) * horizontal_spacing
                    mid_x = base_mid_x + offset

                    if mid_x < safe_min_x:
                        mid_x = safe_min_x
                    elif mid_x > safe_max_x:
                        mid_x = safe_max_x

                    x_start = x1 + node_size / 2
                    y_start = y1

                    x_end = x2 - node_size / 2
                    y_end = y2

                    x_mid1, y_mid1 = mid_x, y1
                    x_mid2, y_mid2 = mid_x, y2

                    ax.plot([x_start, x_mid1], [y_start, y_mid1], linewidth=0.8)
                    ax.plot([x_mid1, x_mid2], [y_mid1, y_mid2], linewidth=0.8)
                    ax.plot([x_mid2, x_end], [y_mid2, y_end], linewidth=0.8)
        else:
            raise ValueError(f"Unknown orientation: {orientation}")

        ax.set_aspect("equal")
        ax.axis("off")

        margin_units = node_size * (3.0 * spacing_scale)
        ax.set_xlim(min(all_x) - margin_units, max(all_x) + margin_units)
        ax.set_ylim(min(all_y) - margin_units, max(all_y) + margin_units)

        plt.tight_layout()
        return fig

    def save_png(
        self,
        tree: SkillTree,
        filename: str,
        orientation: str = "top_down",
        dpi: int = 200,
    ) -> None:
        fig = self.create_figure(tree, orientation=orientation)
        fig.savefig(filename, dpi=dpi)
        plt.close(fig)
