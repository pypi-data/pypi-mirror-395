from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from enum import Enum
from pydantic import BaseModel, Field

class scrna_mcp_tools(str, Enum):
    run_cell_quality_control = 'run_cell_quality_control'
    run_doublet_filter = 'run_doublet_filter'
    run_normalization = 'run_normalization'
    run_data_integration = 'run_data_integration'
    run_find_hvg = 'run_find_hvg'
    run_data_reduction = 'run_data_reduction'
    run_cell_cluster = 'run_cell_cluster'
    run_find_marker = 'run_find_marker'
    run_cell_annotation = 'run_cell_annotation'
    run_deg = 'run_deg'
    run_trajectory = 'run_trajectory'
    run_cellchat = 'run_cellchat'
    run_transcription_factor_activity = 'run_transcription_factor_activity'
    run_RNA_velocity = 'run_RNA_velocity'
    run_go_enrichment = 'run_go_enrichment'
    run_kegg_enrichment = 'run_kegg_enrichment'
    run_gsva_enrichment = 'run_gsva_enrichment'


class run_cell_quality_control_inputs(BaseModel):
    seurat_obj: str = Field(description = '质量控制前的 Seurat 对象文件路径（.rds 格式，需包含原始计数矩阵）')
    nFeature_RNA: int = Field(description = '基因数量 **小于** 该值的细胞将被丢弃（*建议根据数据分布调整；新鲜组织通常 200-500，冷冻样本可降至 100-200*）')
    nCount_RNA: int = Field(description = 'UMI 数量 **小于** 该值的细胞将被丢弃（*建议根据数据分布调整；高深度测序可设为 500-2000*）')
    mt_percent: float = Field(description = '线粒体基因占比 **超过** 该值的细胞将被丢弃')
    hb_percent: float = Field(description = '红细胞基因占比 **超过** 该值的细胞将被丢弃（*仅适用于血液/骨髓样本；非血液样本建议设为 `None`*）')

class run_cell_quality_control_outputs(BaseModel):
    seurat_obj: str = Field(description = '质量控制后的 Seurat 对象文件路径（.rds 格式）')

def run_cell_quality_control(
        seurat_obj,
        nFeature_RNA = 200,
        nCount_RNA = 800,
        mt_percent = 15,
        hb_percent = 0.1
    ) -> run_cell_quality_control_outputs:
    return run_cell_quality_control_outputs(
        seurat_obj = f'/output_datas/qc_seurat.rds'
    )


class run_doublet_filter_inputs(BaseModel):
    seurat_obj: str = Field(description = '经过初步质控的 Seurat 对象文件路径（.rds 格式）')
    method: str = Field(description = '双细胞检测方法')
    expected_doublet_rate: float = Field(description = '预期双细胞率，通常为总细胞数的 5-10%。与细胞加载浓度正相关，高浓度样本可设为 0.08-0.10')
    pN: float = Field(description = '人工双细胞占真实细胞的比例，通常无需调整')
    pK: float = Field(description = '最近邻比例，默认 None 表示自动计算，也可手动指定如 "0.005"、"0.01" 等，通常自动计算即可')

class run_doublet_filter_outputs(BaseModel):
    seurat_obj: str = Field(description = '双细胞过滤后的 Seurat 对象文件路径（.rds 格式）')

def run_doublet_filter(
        seurat_obj,
        method = "DoubletFinder",
        expected_doublet_rate = 0.05,
        pN = 0.25,
        pK = None
    ) -> run_doublet_filter_outputs:
    return run_doublet_filter_outputs(
        seurat_obj = f'/output_datas/doublet_filtered_seurat.rds'
    )


class run_normalization_inputs(BaseModel):
    seurat_obj: str = Field(description = '质控后（及双细胞过滤后）的 Seurat 对象文件路径（.rds 格式）')
    method: str = Field(description = '标准化方法')
    scale_factor: int = Field(description = '仅用于 "LogNormalize" 方法。将每个细胞的总 UMI 数缩放至该值，然后进行 log(1+x) 转换')
    variable_features_n: int = Field(description = '仅用于 "SCTransform" 方法。指定保留的高可变基因数量，通常2000-5000')
    conserve_memory: bool = Field(description = '仅用于 "SCTransform" 方法。内存节省模式，适用于大型数据集（>5万细胞），但可能略降低精度')

class run_normalization_outputs(BaseModel):
    seurat_obj: str = Field(description = '标准化后的 Seurat 对象文件路径（.rds 格式）')

def run_normalization(
        seurat_obj,
        method = "LogNormalize",
        scale_factor = 10000,
        variable_features_n = 2000,
        conserve_memory = False
    ) -> run_normalization_outputs:
    return run_normalization_outputs(
        seurat_obj = f'/output_datas/normalized_seurat.rds'
    )


class run_data_integration_inputs(BaseModel):
    seurat_obj_list: str = Field(description = '待整合的 Seurat 对象文件路径列表（.rds 格式文件路径列表）')
    method: str = Field(description = '整合方法')
    batch_key: str = Field(description = '批次信息的元数据列名')
    nfeatures: int = Field(description = '用于整合的特征（基因）数量')
    npcs: int = Field(description = '用于整合的 PCA 维度数')
    k_filter: int = Field(description = '用于寻找锚点的最近邻数量')
    dims: int = Field(description = '用于整合的 PCA 维度最大范围')
    harmony_theta: float = Field(description = 'harmony 专用参数，多样性惩罚强度。值越大批次校正越强')
    harmony_lambda: float = Field(description = 'harmony 专用参数，ridge 回归惩罚。用于调整特征重要性')
    max_iter: int = Field(description = '最大迭代次数')

class run_data_integration_outputs(BaseModel):
    seurat_obj: str = Field(description = '整合后的 Seurat 对象文件路径（.rds格式）')

def run_data_integration(
        seurat_obj_list,
        method = "harmony",
        batch_key = "batch",
        nfeatures = 2000,
        npcs = 30,
        k_filter = 200,
        dims = 30,
        harmony_theta = 2,
        harmony_lambda = 1,
        max_iter = 10
    ) -> run_data_integration_outputs:
    return run_data_integration_outputs(
        seurat_obj = f'/output_datas/integrated_seurat.rds'
    )


class run_find_hvg_inputs(BaseModel):
    seurat_obj: str = Field(description = '标准化后的 Seurat 对象文件路径（.rds 格式）')
    nfeatures: int = Field(description = '选择的高可变基因数量。通常 2000-5000，大型数据集可增至 8000')
    selection_method: str = Field(description = '筛选方法')

class run_find_hvg_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含高可变基因标记的 Seurat 对象文件路径（.rds 格式）')

def run_find_hvg(
        seurat_obj,
        nfeatures = 2000,
        selection_method = "vst"
    ) -> run_find_hvg_outputs:
    return run_find_hvg_outputs(
        seurat_obj = f'/output_datas/hvg_seurat.rds'
    )


class run_data_reduction_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含高可变基因的 Seurat 对象文件路径（.rds 格式）')
    methods: list[str] = Field(description = '降维方法列表')
    npcs: int = Field(description = 'PCA 计算的主成分数量。通常 30-50，足够捕获主要变异')
    dimensions: int = Field(description = '用于后续分析（如聚类、UMAP）的 PCA 维度数。通常 10-30，应基于 PCA 肘部图确定')
    reduction: str = Field(description = '用于非线性降维的基础降维结果。通常为 "pca"')
    umap_metric: str = Field(description = 'UMAP 使用的距离度量')
    tsne_perplexity: float = Field(description = ' t-SNE 的困惑度参数，控制近邻数量。通常 5-50，值越大考虑越多的全局结构')

class run_data_reduction_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含降维结果的 Seurat 对象文件路径（.rds 格式）')

def run_data_reduction(
        seurat_obj,
        methods = ["pca", "umap"],
        npcs = 50,
        dimensions = 30,
        reduction = "pca",
        umap_metric = "cosine",
        tsne_perplexity = 30
    ) -> run_data_reduction_outputs:
    return run_data_reduction_outputs(
        seurat_obj = f'/output_datas/reduced_seurat.rds'
    )


class run_cell_cluster_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含降维结果的 Seurat 对象文件路径（.rds 格式）')
    methods: str = Field(description = '聚类算法')
    resolution: float = Field(description = '聚类分辨率参数，控制簇的粒度。值越大，簇越多越细')
    algorithm: int = Field(description = 'Louvain 算法变体。1=原始Louvain，2=SLM，3=Leiden（仅当`method="louvain"`时有效）')
    k_param: int = Field(description = '构建 k 近邻图时使用的最近邻数量。值越大，聚类越稳定但可能模糊边界')

class run_cell_cluster_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含聚类标签的 Seurat 对象文件路径（.rds 格式）')

def run_cell_cluster(
        seurat_obj,
        methods = "louvain",
        resolution = 0.8,
        algorithm = 1,
        k_param = 20
    ) -> run_cell_cluster_outputs:
    return run_cell_cluster_outputs(
        seurat_obj = f'/output_datas/clustered_seurat.rds'
    )


class run_find_marker_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含聚类标签的 Seurat 对象文件路径（.rds 格式）')
    ident_1: str = Field(description = '比较组 1 的簇 ID 或细胞类型。如不指定，则进行所有簇的一对多比较（每个簇 vs 其余所有细胞）')
    ident_2: str = Field(description = '比较组 2 的簇 ID 或细胞类型。如指定，则进行 `ident_1` vs `ident_2` 的直接比较')
    min_pct: float = Field(description = '基因在簇中的最小表达比例。要求基因至少在 `min_pct` 比例的簇内细胞中表达')
    logfc_threshold: float = Field(description = '对数倍数变化阈值。要求基因的平均表达差异至少达到该值（以 log2 scale 计）')
    test_use: str = Field(description = '统计检验方法')
    threshold: float = Field(description = '调整后p值（FDR）阈值。仅返回 FDR 小于此值的基因')

class run_find_marker_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含标记基因分析结果的 Seurat 对象文件路径（.rds 格式）')
    marker_result_file: str = Field(description = '标记基因结果文件（.csv 格式），每个簇的 top 标记基因列表')

def run_find_marker(
        seurat_obj,
        ident_1 = None,
        ident_2 = None,
        min_pct = 0.25,
        logfc_threshold = 0.25,
        test_use = "wilcox",
        threshold = 0.05
    ) -> run_find_marker_outputs:
    return run_find_marker_outputs(
        seurat_obj = f'/output_datas/marker_seurat.rds',
        marker_result_file = f'/output_datas/marker_result.csv'
    )


class run_cell_annotation_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含标记基因分析结果的 Seurat 对象文件路径（.rds 格式）')
    method: str = Field(description = '注释方法')
    reference: str = Field(description = '参考数据库名称')
    marker_db: str = Field(description = '自定义标记基因数据库文件路径')
    cluster_col: str = Field(description = '包含聚类结果的列名')
    min_score: float = Field(description = '自动注释的最小置信度分数（0-1之间）。仅保留置信度高于此值的注释')
    tissue_type: str = Field(description = '组织类型，用于筛选相关的细胞类型')

class run_cell_annotation_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含细胞类型注释的 Seurat 对象文件路径（.rds 格式）')
    cell_anno_file: str = Field(description = '细胞类型注释结果文件（.csv 格式）')

def run_cell_annotation(
        seurat_obj,
        method = "manual",
        reference = "HumanPrimaryCellAtlas",
        marker_db = None,
        cluster_col = "seurat_clusters",
        min_score = 0.5,
        tissue_type = "PBMC"
    ) -> run_cell_annotation_outputs:
    return run_cell_annotation_outputs(
        seurat_obj = f'/output_datas/annotated_seurat.rds',
        cell_anno_file = f'/output_datas/cell_anno.csv'
    )


class run_deg_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含细胞类型注释的 Seurat 对象文件路径（.rds 格式）')
    cell_type: str = Field(description = '限制分析的细胞类型。如不指定，则使用所有细胞')
    min_pct: float = Field(description = '基因在任一组中的最小表达比例。低于此比例的基因将被过滤')
    logfc_threshold: float = Field(description = '对数倍数变化阈值')
    test_use: str = Field(description = '统计检验方法')
    threshold: float = Field(description = '调整后 p 值阈值')

class run_deg_outputs(BaseModel):
    deg_result_file: str = Field(description = '差异表达分析结果文件（.csv 格式）')

def run_deg(
        seurat_obj,
        cell_type = None,
        min_pct = 0.1,
        logfc_threshold = 0.25,
        test_use = "wilcox",
        threshold = 0.05
    ) -> run_deg_outputs:
    return run_deg_outputs(
        deg_result_file = f'/output_datas/deg_result.csv'
    )


class run_trajectory_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含细胞类型注释的 Seurat 对象文件路径（.rds 格式）')
    method: str = Field(description = '轨迹推断方法')
    root_cells: str = Field(description = '轨迹起点的细胞 ID 或细胞类型。如不指定，算法将尝试自动推断')
    gene_selection_method: str = Field(description = '用于轨迹分析的基因选择方法')
    num_paths: int = Field(description = '预期轨迹路径数（仅 slingshot 方法）。如不指定自动推断')
    reduce_dimension: str = Field(description = '轨迹可视化的降维方法')

class run_trajectory_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含轨迹信息的 Seurat/Monocle 对象文件路径（.rds 格式）')
    pseudotime_result_file: str = Field(description = '轨迹结果文件（.csv 格式）')
    pseudotime_gene_file: str = Field(description = '轨迹动态基因列表（.csv 格式）')

def run_trajectory(
        seurat_obj,
        method = "monocle3",
        root_cells = None,
        gene_selection_method = "seurat",
        num_paths = None,
        reduce_dimension = "UMAP"
    ) -> run_trajectory_outputs:
    return run_trajectory_outputs(
        seurat_obj = f'/output_datas/trajectory_seurat.rds',
        pseudotime_result_file = f'/output_datas/pseudotime_result.csv',
        pseudotime_gene_file = f'/output_datas/pseudotime_gene.csv'
    )


class run_cellchat_inputs(BaseModel):
    seurat_obj: str = Field(description = '包含细胞类型注释的 Seurat 对象文件路径（.rds 格式）')
    group_by: str = Field(description = '细胞分组依据，通常是细胞类型注释列')
    species: str = Field(description = '物种。支持："human"、"mouse"。非此二物种需提供自定义数据库')
    ligand_receptor_db: str = Field(description = '自定义配体-受体数据库文件路径（.rds格式）')
    min_cells_per_group: int = Field(description = '每组（细胞类型）最少细胞数。少于该数的组将被排除')
    n_permutations: int = Field(description = '显著性检验的置换次数。值越大结果越稳定但计算越慢')
    prob_threshold: float = Field(description = '相互作用概率阈值。仅保留概率高于此值的相互作用')
    remove_self: bool = Field(description = '是否移除同一细胞类型内的自相互作用')
    communication_type: str = Field(description = '通讯类型')

class run_cellchat_outputs(BaseModel):
    seurat_obj: str = Field(description = 'CellChat 对象文件路径（.rds 格式），包含完整的细胞通讯分析结果')
    cell_chat_file: str = Field(description = '细胞通讯网络结果文件（.csv 格式）')

def run_cellchat(
        seurat_obj,
        group_by = "cell_type",
        species = "human",
        ligand_receptor_db = None,
        min_cells_per_group = 10,
        n_permutations = 100,
        prob_threshold = 0.05,
        remove_self = True,
        communication_type = "autocrine_paracrine"
    ) -> run_cellchat_outputs:
    return run_cellchat_outputs(
        seurat_obj = f'/output_datas/cellchat_seurat.rds',
        cell_chat_file = f'/output_datas/cellchat_result.csv'
    )


class run_transcription_factor_activity_inputs(BaseModel):
    seurat_obj: str = Field(description = '标准化后的 Seurat 对象文件路径（.rds 格式）')
    method: str = Field(description = '分析方法')
    species: str = Field(description = '物种。支持："human"、"mouse"')
    confidence_level: str = Field(description = 'TF-靶基因相互作用的置信度级别')
    minsize: int = Field(description = '每个 TF 的最小靶基因数。靶基因数少于此值的 TF 将被排除')
    nes_threshold: float = Field(description = '富集分数阈值。仅保留 NES（标准化富集分数）绝对值高于此值的 TF')
    regulons_db: str = Field(description = '自定义调控子数据库文件路径')

class run_transcription_factor_activity_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含 TF 活性分数的 Seurat 对象文件路径（.rds 格式）')
    tf_activity_file: str = Field(description = 'TF 活性结果文件（.csv 格式）')

def run_transcription_factor_activity(
        seurat_obj,
        method = "dorothea",
        species = "human",
        confidence_level = "ABC",
        minsize = 5,
        nes_threshold = 0,
        regulons_db = None
    ) -> run_transcription_factor_activity_outputs:
    return run_transcription_factor_activity_outputs(
        seurat_obj = f'/output_datas/tf_activity_seurat.rds',
        tf_activity_file = f'/output_datas/tf_activity_result.csv'
    )


class run_RNA_velocity_inputs(BaseModel):
    seurat_obj: str = Field(description = '标准化后的 Seurat 对象文件路径（.rds 格式）。必须包含未剪接和已剪接计数矩阵')
    spliced_assay: str = Field(description = '已剪接转录本 assay 的名称')
    unspliced_assay: str = Field(description = '未剪接转录本 assay 的名称')
    method: str = Field(description = '分析方法')
    mode: int = Field(description = 'scVelo 的计算模式')
    n_top_genes: float = Field(description = '用于分析的高可变基因数')
    min_shared_counts: str = Field(description = '细胞间最小共享计数，用于构建 k 近邻图')
    velocity_plot_type: str = Field(description = '速率可视化类型')

class run_RNA_velocity_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含 RNA 速率结果的 Seurat 对象文件路径（.rds 格式）')
    rna_velocity_file: str = Field(description = '速率分析结果文件（.csv 格式）')

def run_RNA_velocity(
        seurat_obj,
        spliced_assay = "spliced",
        unspliced_assay = "unspliced",
        method = "scvelo",
        mode = "dynamical",
        n_top_genes = 2000,
        min_shared_counts = 30,
        velocity_plot_type = "stream"
    ) -> run_RNA_velocity_outputs:
    return run_RNA_velocity_outputs(
        seurat_obj = f'/output_datas/RNA_velocity_seurat.rds',
        rna_velocity_file = f'/output_datas/RNA_velocity_result.csv'
    )


class run_go_enrichment_inputs(BaseModel):
    gene_list: str = Field(description = '输入基因列表文件路径（如差异表达基因）')
    organism: str = Field(description = '物种')
    pvalue_cutoff: float = Field(description = 'p 值阈值（未校正）')
    qvalue_cutoff: float = Field(description = 'q 值阈值（FDR 校正后）')

class run_go_enrichment_outputs(BaseModel):
    go_result_file: str = Field(description = 'GO 富集分析结果文件（.csv 格式）')

def run_go_enrichment(
        gene_list,
        organism = "human",
        pvalue_cutoff = 0.05,
        qvalue_cutoff = 0.05
    ) -> run_go_enrichment_outputs:
    return run_go_enrichment_outputs(
        go_result_file = f'/output_datas/go_result.csv'
    )


class run_kegg_enrichment_inputs(BaseModel):
    gene_list: str = Field(description = '输入基因列表文件路径（如差异表达基因）')
    organism: str = Field(description = '物种')
    pvalue_cutoff: float = Field(description = 'p 值阈值（未校正）')
    qvalue_cutoff: float = Field(description = 'q 值阈值（FDR 校正后）')

class run_kegg_enrichment_outputs(BaseModel):
    kegg_result_file: str = Field(description = 'KEGG 富集分析结果文件（.csv 格式）')

def run_kegg_enrichment(
        gene_list,
        organism = "human",
        pvalue_cutoff = 0.05,
        qvalue_cutoff = 0.05
    ) -> run_kegg_enrichment_outputs:
    return run_kegg_enrichment_outputs(
        kegg_result_file = f'/output_datas/kegg_result.csv'
    )


class run_gsva_enrichment_inputs(BaseModel):
    seurat_obj: str = Field(description = '标准化后的 Seurat 对象文件路径（.rds 格式）')
    organism: str = Field(description = '物种')
    method: str = Field(description = '计算方法')
    kcdf: str = Field(description = '核函数选择')

class run_gsva_enrichment_outputs(BaseModel):
    seurat_obj: str = Field(description = '包含 GSVA 分数的 Seurat 对象文件路径（.rds 格式），新增 assay 存储通路活性分数')

def run_gsva_enrichment(
        seurat_obj,
        organism = "human",
        method = "gsva",
        kcdf = "Gaussian"
    ) -> run_gsva_enrichment_outputs:
    return run_gsva_enrichment_outputs(
        seurat_obj = f'/output_datas/gsva_seurat.csv'
    )


async def mcp_server() -> None:
    server = Server("scRNA MCP server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=scrna_mcp_tools.run_cell_quality_control,
                description=""" 单细胞数据质量控制，过滤低质量细胞 """,
                inputSchema=run_cell_quality_control_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_doublet_filter,
                description=""" 多重细胞过滤，识别并去除单个液滴中包含两个或多个细胞的“双联体” """,
                inputSchema=run_doublet_filter_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_normalization,
                description=""" 数据标准化，消除细胞间测序深度（总 UMI 数）的技术差异，使基因表达量在不同细胞间具有可比性 """,
                inputSchema=run_normalization_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_data_integration,
                description=""" 多样本/多批次单细胞数据整合，校正技术批次效应 """,
                inputSchema=run_data_integration_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_find_hvg,
                description=""" 高可变基因筛选，识别细胞间表达变异最大的基因 """,
                inputSchema=run_find_hvg_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_data_reduction,
                description=""" 数据降维，将高维基因表达数据（通常数千个高可变基因）压缩至低维空间（通常2-50维），以可视化数据结构和进行下游分析 """,
                inputSchema=run_data_reduction_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_cell_cluster,
                description=""" 细胞聚类分析，基于降维后的基因表达相似性将细胞分组，识别不同的细胞类型、状态或亚群 """,
                inputSchema=run_cell_cluster_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_find_marker,
                description=""" 差异表达分析，为每个细胞簇寻找特异性高表达的标记基因 """,
                inputSchema=run_find_marker_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_cell_annotation,
                description=""" 细胞类型注释，将每个细胞簇与已知的细胞类型相关联 """,
                inputSchema=run_cell_annotation_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_deg,
                description=""" 差异表达分析，系统比较不同条件、处理或细胞状态间的基因表达差异 """,
                inputSchema=run_deg_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_trajectory,
                description=""" 拟时序分析，推断细胞分化、激活或状态转变的动态轨迹 """,
                inputSchema=run_trajectory_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_cellchat,
                description=""" 细胞通讯分析，预测不同细胞群体间的配体-受体相互作用 """,
                inputSchema=run_cellchat_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_transcription_factor_activity,
                description=""" 转录因子活性分析，基于转录因子（TF）靶基因的表达模式，推断 TF 的调控活性 """,
                inputSchema=run_transcription_factor_activity_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_RNA_velocity,
                description=""" RNA速率分析，通过未剪接（新生）与已剪接（成熟）mRNA 的比例，预测细胞的未来状态和基因表达的动态变化 """,
                inputSchema=run_RNA_velocity_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_go_enrichment,
                description=""" GO（Gene Ontology）富集分析，分析基因集（如差异表达基因）在 Gene Ontology 功能类别中的过度表示 """,
                inputSchema=run_go_enrichment_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_kegg_enrichment,
                description=""" KEGG（Kyoto Encyclopedia of Genes and Genomes）富集分析，分析基因集在 KEGG 通路数据库中的过度表示 """,
                inputSchema=run_kegg_enrichment_inputs.model_json_schema(),
            ),
            Tool(
                name=scrna_mcp_tools.run_gsva_enrichment,
                description=""" 基因集变异分析，在单细胞水平评估预定义基因集（如通路、功能模块、细胞状态特征）的活性 """,
                inputSchema=run_gsva_enrichment_inputs.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        match name:
            case scrna_mcp_tools.run_cell_quality_control:
                return run_cell_quality_control(arguments)

            case scrna_mcp_tools.run_doublet_filter:
                return run_doublet_filter(arguments)

            case scrna_mcp_tools.run_normalization:
                return run_normalization(arguments)
            
            case scrna_mcp_tools.run_data_integration:
                return run_data_integration(arguments)

            case scrna_mcp_tools.run_find_hvg:
                return run_find_hvg(arguments)

            case scrna_mcp_tools.run_data_reduction:
                return run_data_reduction(arguments)

            case scrna_mcp_tools.run_cell_cluster:
                return run_cell_cluster(arguments)

            case scrna_mcp_tools.run_find_marker:
                return run_find_marker(arguments)

            case scrna_mcp_tools.run_cell_annotation:
                return run_cell_annotation(arguments)

            case scrna_mcp_tools.run_deg:
                return run_deg(arguments)

            case scrna_mcp_tools.run_trajectory:
                return run_trajectory(arguments)

            case scrna_mcp_tools.run_cellchat:
                return run_cellchat(arguments)

            case scrna_mcp_tools.run_transcription_factor_activity:
                return run_transcription_factor_activity(arguments)

            case scrna_mcp_tools.run_RNA_velocity:
                return run_RNA_velocity(arguments)

            case scrna_mcp_tools.run_go_enrichment:
                return run_go_enrichment(arguments)

            case scrna_mcp_tools.run_kegg_enrichment:
                return run_kegg_enrichment(arguments)
            
            case scrna_mcp_tools.run_gsva_enrichment:
                return run_gsva_enrichment(arguments)
            
            case _:
                raise ValueError(f"Unknown tool: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
