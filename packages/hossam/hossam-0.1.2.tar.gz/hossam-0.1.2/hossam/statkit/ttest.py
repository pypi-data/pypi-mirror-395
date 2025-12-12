def my_ttest(df,
             test_type="one",          # ← 사용자 지정 필수: one / paired / independent
             plot_distribution=True,
             plot_result=True,
             interpret_style="report",
             auto_nonparametric=True,
             markdown=True,
             dpi=200,
             alpha=0.05):

    """통합형 T-Test 분석 함수.

    정규성 및 등분산성 가정을 자동으로 검토하고, 적절한 T-Test 또는 비모수 검정을 수행합니다.
    데이터 분포 시각화, 검정 결과 시각화, 그리고 상세한 해석을 제공합니다.

    Args:
        df (pd.DataFrame): 분석할 데이터프레임.
            - 단일표본: 1개 컬럼 필요
            - 대응표본/독립표본: 2개 컬럼 필요
        test_type (str): 검정 유형. "one" (단일표본), "paired" (대응표본),
            "independent" (독립표본) 중 선택. 기본값은 "one".
        plot_distribution (bool): 데이터 분포 및 신뢰구간 시각화 여부. 기본값은 True.
        plot_result (bool): 검정 결과 박스플롯 시각화 여부 (단일표본 제외). 기본값은 True.
        interpret_style (str): 해석문 스타일. "report" (상세한 논문형), "apa" (APA 스타일),
            또는 간단한 요약 중 선택. 기본값은 "report".
        auto_nonparametric (bool): 정규성 가정 위반 시 자동으로 비모수 검정 적용 여부.
            기본값은 True.
        markdown (bool): 결과를 마크다운 형식으로 출력할지 여부. 기본값은 True.
        dpi (int): 그래프 해상도 설정. 기본값은 200.
        alpha (float): 유의수준. 기본값은 0.05.

    Returns:
        None: 함수는 결과를 직접 출력하고 시각화합니다.

    Raises:
        ValueError: test_type이 유효하지 않거나, 컬럼 수가 검정 유형에 맞지 않을 때.

    Examples:
        >>> # 단일표본 T-검정
        >>> df_one = pd.DataFrame({'score': [75, 80, 85, 90, 95]})
        >>> my_ttest(df_one, test_type="one")

        >>> # 대응표본 T-검정
        >>> df_paired = pd.DataFrame({'before': [70, 75, 80], 'after': [80, 85, 90]})
        >>> my_ttest(df_paired, test_type="paired")

        >>> # 독립표본 T-검정
        >>> df_indep = pd.DataFrame({'group_A': [70, 75, 80], 'group_B': [85, 90, 95]})
        >>> my_ttest(df_indep, test_type="independent")

    Note:
        - 정규성 검정: D'Agostino의 정규성 검정 사용
        - 등분산성 검정: 정규성 충족 시 Bartlett 검정, 미충족 시 Levene 검정
        - 비모수 대안: Wilcoxon (단일/대응표본), Mann-Whitney U (독립표본)
        - 효과크기: Cohen's d 계산 및 해석 제공
    """

    # -------------------------------------------------------------
    # 0) 기본 import
    # -------------------------------------------------------------
    import numpy as np
    import seaborn as sb
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    from math import sqrt
    from pandas import DataFrame, melt
    from scipy.stats import (
        ttest_rel, ttest_ind, ttest_1samp,
        wilcoxon, mannwhitneyu,
        normaltest, levene, bartlett
    )
    from scipy.stats import t
    from statannotations.Annotator import Annotator
    from IPython.display import display



    # -------------------------------------------------------------
    # 2) 입력 검증
    # -------------------------------------------------------------
    fields = df.columns.tolist()
    k = len(fields)

    valid_types = ["one", "paired", "independent"]
    if test_type not in valid_types:
        raise ValueError(f"test_type은 {valid_types} 중 하나여야 합니다.")

    if test_type == "one" and k != 1:
        raise ValueError("단일표본(one)은 반드시 1개의 컬럼만 있어야 합니다.")

    if test_type in ["paired", "independent"] and k != 2:
        raise ValueError(f"{test_type} 검정은 반드시 2개의 컬럼이 필요합니다.")

    f0 = fields[0]
    f1 = fields[1] if k == 2 else None

    # -------------------------------------------------------------
    # 3) 분포 시각화
    # -------------------------------------------------------------
    if plot_distribution:
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")

        fig, ax = plt.subplots(1, 1, figsize=(1280 / dpi, 720 / dpi), dpi=dpi)

        for c in fields:
            sb.kdeplot(data=df, x=c, fill=False, alpha=0.6)

            mean = df[c].mean()
            std = df[c].std(ddof=1)
            se = std / sqrt(len(df[c]))

            clevel = 0.95
            dof = len(df[c]) - 1
            cmin, cmax = t.interval(clevel, dof, loc=mean, scale=se)
            ymin, ymax = ax.get_ylim()

            ax.axvline(cmin, linestyle=":", linewidth=0.5)
            ax.axvline(cmax, linestyle=":", linewidth=0.5)
            ax.fill_between([cmin, cmax], 0, ymax, alpha=0.15)
            ax.axvline(mean, linestyle="--", linewidth=1)

            # 한글 텍스트 표시 시 폰트 명시적 지정
            # font_prop = fm.FontProperties(fname=font_path) if os.path.exists(font_path) else None
            ax.text((cmin + cmax)/2, ymax,
                    f"[{c}] {cmin:.1f} ~ {cmax:.1f}",
                    ha="center", va="bottom", fontsize=7, color="red")

        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        plt.close()

    # -------------------------------------------------------------
    # 4) 정규성 검사 (두 변수 모두)
    # -------------------------------------------------------------
    report = []
    normal_ok = True
    for c in fields:
        s, p = normaltest(df[c])
        normal_ok = normal_ok and (p > alpha)

        report.append({
            "field": c,
            "statistic": s,
            "p-value": p,
            "result": normal_ok
        })

    # -------------------------------------------------------------
    # 5) 등분산성 검사 (independent + 정규성 충족 시 Bartlett, 아니면 Levene)
    # -------------------------------------------------------------
    equal_var = True
    var_test_name = None

    if test_type == "independent":  # method None → 모수검정 예정

        if normal_ok:
            # 🔥 정규성 충족 → Bartlett
            stat_var, p_var = bartlett(df[f0], df[f1])
            equal_var = p_var > alpha
            var_test_name = "Bartlett"

        else:
            # 🔥 정규성 불충족 → Levene
            stat_var, p_var = levene(df[f0], df[f1], center="median")
            equal_var = p_var > alpha
            var_test_name = "Levene"

        report.append({
            "field": var_test_name,
            "statistic": stat_var,
            "p-value": p_var,
            "result": p_var > 0.05
        })

    if report:
        print("\n===== [가정 확인] =====")
        display(DataFrame(report))

    # -------------------------------------------------------------
    # 6) 정규성 실패 시 비모수로 자동 전환
    # -------------------------------------------------------------
    method = None
    nonparametric_reason = None

    if not normal_ok and auto_nonparametric:

        if test_type == "one":
            method = "wilcoxon"
            nonparametric_reason = "정규성 실패 → Wilcoxon 단일표본 적용"

        elif test_type == "paired":
            method = "wilcoxon"
            nonparametric_reason = "정규성 실패 → Wilcoxon 대응표본 적용"

        elif test_type == "independent":
            method = "mannwhitney"
            nonparametric_reason = "정규성 실패 → Mann–Whitney 독립표본 적용"

    # -------------------------------------------------------------
    # 7) 본 검정 수행
    # -------------------------------------------------------------
    results = []
    alternative_list = ["two-sided", "less", "greater"]

    for a in alternative_list:

        # --- 단일표본 ---
        if test_type == "one":
            if method == "wilcoxon":
                s, p = wilcoxon(df[f0], alternative=a)
                test_label = "Wilcoxon signed-rank test"
                annotator_test = None
            else:
                s, p = ttest_1samp(df[f0], 0, alternative=a)
                test_label = "one-sample t-test"
                annotator_test = None

            interp = f"μ({f0}) {'=' if p>alpha else '≠'} 0"

        # --- 대응표본 ---
        elif test_type == "paired":

            if method == "wilcoxon":
                s, p = wilcoxon(df[f0], df[f1], alternative=a)
                test_label = "Wilcoxon signed-rank test"
                annotator_test = "Wilcoxon"

            else:
                s, p = ttest_rel(df[f0], df[f1], alternative=a)
                test_label = "paired t-test"
                annotator_test = "t-test_paired"

            fmt = "μ({f0}) {0} μ({f1})"
            interp = fmt.format("==" if p > alpha else "!=", f0=f0, f1=f1)

        # --- 독립표본 ---
        elif test_type == "independent":

            if method == "mannwhitney":
                s, p = mannwhitneyu(df[f0], df[f1], alternative=a)
                test_label = "Mann–Whitney U test"
                annotator_test = "Mann-Whitney"

            else:
                s, p = ttest_ind(df[f0], df[f1], equal_var=equal_var, alternative=a)

                if equal_var:
                    test_label = "independent t-test"
                    annotator_test = "t-test_ind"
                else:
                    test_label = "Welch t-test"
                    annotator_test = "t-test_welch"

            fmt = "μ({f0}) {0} μ({f1})"
            interp = fmt.format("==" if p > alpha else "!=", f0=f0, f1=f1)

        results.append({
            "alternative": a,
            "statistic": s,
            "p-value": p,
            "H0": p > alpha,
            "interpretation": interp
        })

        # 양측 검정에서 H0 유지되면 방향성 의미 없음 → 종료
        if a == "two-sided" and p > alpha:
            break

    rdf = DataFrame(results).set_index("alternative")

    print("\n===== [검정 결과표] =====")
    display(rdf)

    # -------------------------------------------------------------
    # 8) 시각화 (단일표본 제외)
    # -------------------------------------------------------------
    if plot_result and test_type != "one":
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")

        visual_df = melt(df, value_vars=fields, var_name="group", value_name="value")

        fig, ax = plt.subplots(1, 1, figsize=(1280 / dpi, 720 / dpi), dpi=dpi)
        sb.boxplot(data=visual_df, x="group", y="value", hue="group")

        annotator = Annotator(ax, pairs=[fields], data=visual_df, x="group", y="value")
        annotator.configure(test=annotator_test)
        annotator.apply_and_annotate()

        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        plt.close()

    # -------------------------------------------------------------
    # 9) 논문 수준 해설문 생성
    # -------------------------------------------------------------
    ts = rdf.loc["two-sided"]
    p = ts["p-value"]
    stat = ts["statistic"]

    # 기술통계 계산
    n = len(df)
    if test_type == "one":
        mean1 = df[f0].mean()
        std1 = df[f0].std(ddof=1)
        se1 = std1 / sqrt(n)
        effect_size = mean1 / std1  # Cohen's d for one-sample

    else:
        mean1 = df[f0].mean()
        mean2 = df[f1].mean()
        std1 = df[f0].std(ddof=1)
        std2 = df[f1].std(ddof=1)
        se1 = std1 / sqrt(n)
        se2 = std2 / sqrt(n)

        if test_type == "paired":
            # 대응표본의 경우 차이값의 효과크기
            diff = df[f0] - df[f1]
            mean_diff = diff.mean()
            std_diff = diff.std(ddof=1)
            effect_size = mean_diff / std_diff  # Cohen's d for paired
        else:
            # 독립표본의 경우 pooled standard deviation 사용
            pooled_std = sqrt(((n-1)*std1**2 + (n-1)*std2**2) / (2*n-2))
            effect_size = abs(mean1 - mean2) / pooled_std  # Cohen's d for independent

    # 효과크기 해석
    if abs(effect_size) < 0.2:
        effect_interpretation = "매우 작은"
    elif abs(effect_size) < 0.5:
        effect_interpretation = "작은"
    elif abs(effect_size) < 0.8:
        effect_interpretation = "중간"
    else:
        effect_interpretation = "큰"

    def make_detailed_explanation(style):
        # 연구 설계 및 방법론 부분
        methodology_text = f"본 연구에서는 총 {n}개의 관측값을 대상으로 "

        if test_type == "one":
            methodology_text += f"단일표본 평균이 기준값 0과 차이가 있는지 검증하기 위해 "
        elif test_type == "paired":
            methodology_text += f"두 측정값({f0}, {f1}) 간의 차이를 분석하기 위해 대응표본 설계를 사용하여 "
        else:
            methodology_text += f"두 독립 집단({f0}, {f1}) 간의 평균 차이를 검증하기 위해 "

        # 가정 검토 부분
        assumption_text = ""
        if normal_ok:
            assumption_text = "데이터의 정규성 가정이 충족되어(D'Agostino's normality test, p > 0.05) "
        else:
            assumption_text = "데이터가 정규분포를 따르지 않아(D'Agostino's normality test, p ≤ 0.05) "

        # 등분산성 검정 결과 (독립표본인 경우)
        variance_text = ""
        if test_type == "independent":
            if normal_ok:
                variance_text = f"Bartlett 등분산성 검정 결과 {'등분산 가정이 충족되어' if equal_var else '등분산 가정이 위반되어'} "
            else:
                variance_text = f"Levene 등분산성 검정 결과 {'등분산 가정이 충족되어' if equal_var else '등분산 가정이 위반되어'} "

        # 분석 방법 선택
        method_text = ""
        if method is None:
            if test_type == "one":
                method_text = "일표본 t-검정을"
            elif test_type == "paired":
                method_text = "대응표본 t-검정을"
            else:
                if equal_var:
                    method_text = "독립표본 t-검정을"
                else:
                    method_text = "Welch의 t-검정을"
        else:
            if test_type == "one":
                method_text = "Wilcoxon 부호순위 검정을"
            elif test_type == "paired":
                method_text = "Wilcoxon 부호순위 검정을"
            else:
                method_text = "Mann-Whitney U 검정을"

        method_text += " 실시하였다."

        # 기술통계 결과
        descriptive_text = ""
        if test_type == "one":
            descriptive_text = f"분석 결과, {f0}의 평균은 {mean1:.3f} (SD = {std1:.3f}, SE = {se1:.3f})으로 나타났다. "
        elif test_type == "paired":
            descriptive_text = f"분석 결과, {f0}의 평균은 {mean1:.3f} (SD = {std1:.3f}), {f1}의 평균은 {mean2:.3f} (SD = {std2:.3f})으로 나타났으며, 두 측정값의 평균 차이는 {mean1-mean2:.3f}이었다. "
        else:
            descriptive_text = f"분석 결과, {f0} 집단의 평균은 {mean1:.3f} (SD = {std1:.3f}, SE = {se1:.3f}), {f1} 집단의 평균은 {mean2:.3f} (SD = {std2:.3f}, SE = {se2:.3f})으로 나타났으며, 두 집단 간 평균 차이는 {abs(mean1-mean2):.3f}이었다. "

        # 통계적 유의성 및 효과크기
        significance_text = f"통계 검정 결과, "
        if p < alpha:
            if test_type == "one":
                significance_text += f"{f0}의 평균이 0과 통계적으로 유의한 차이를 보였다"
            elif test_type == "paired":
                significance_text += f"{f0}과 {f1} 간에 통계적으로 유의한 차이가 발견되었다"
            else:
                significance_text += f"{f0}과 {f1} 집단 간에 통계적으로 유의한 차이가 발견되었다"
        else:
            if test_type == "one":
                significance_text += f"{f0}의 평균이 0과 통계적으로 유의한 차이를 보이지 않았다"
            elif test_type == "paired":
                significance_text += f"{f0}과 {f1} 간에 통계적으로 유의한 차이가 발견되지 않았다"
            else:
                significance_text += f"{f0}과 {f1} 집단 간에 통계적으로 유의한 차이가 발견되지 않았다"

        # 검정통계량 및 p값 보고
        if method is None:
            significance_text += f" (t = {stat:.3f}, p = {p:.4f})"
        else:
            if "Wilcoxon" in test_label:
                significance_text += f" (W = {stat:.3f}, p = {p:.4f})"
            else:
                significance_text += f" (U = {stat:.3f}, p = {p:.4f})"

        # 효과크기 및 해석
        effect_text = f". 효과크기(Cohen's d)는 {effect_size:.3f}으로, 이는 {effect_interpretation} 효과크기에 해당한다."

        # 연구 제한점 및 해석상 주의사항
        limitation_text = f"본 연구는 {n}개의 표본을 기반으로 하였으며, "
        if not normal_ok and method is not None:
            limitation_text += "정규성 가정이 충족되지 않아 비모수 검정을 적용하였다. "
        if test_type == "independent" and not equal_var and method is None:
            limitation_text += "등분산성 가정이 위배되어 Welch의 보정된 t-검정을 적용하였다. "

        limitation_text += f"유의수준은 α = {alpha}로 설정하였다. 따라서 결과 해석 시 Type I 오류의 가능성을 고려해야 한다."

        # 비모수 검정 적용 시 추가 설명
        nonparametric_note = ""
        if nonparametric_reason:
            nonparametric_note = f"\n\n※ 주의사항: {nonparametric_reason} 따라서 중위수 기반의 비모수 검정 결과로 해석하였으며, 모수적 가정에 기반한 일반화에는 제약이 있다."

        # 최종 해설문 조합
        if style == "report":
            full_text = (
                methodology_text + assumption_text + variance_text + method_text + "\n\n" +
                descriptive_text + significance_text + effect_text + "\n\n" +
                limitation_text + nonparametric_note
            )
        elif style == "apa":
            # APA 스타일 간소화 버전
            full_text = (
                f"A {'one-sample' if test_type == 'one' else test_type + ' samples'} "
                f"{'t-test' if method is None else 'non-parametric test'} was conducted. " +
                descriptive_text.replace('분석 결과, ', '').replace('으로 나타났다', '').replace('이었다', '') +
                significance_text.replace('통계 검정 결과, ', '').replace('발견되었다', 'was found').replace('보였다', 'was observed').replace('발견되지 않았다', 'was not found') +
                f", Cohen's d = {effect_size:.3f} ({effect_interpretation} effect size)."
            )
        else:
            # 간단한 버전
            full_text = f"{test_label} → stat={stat:.3f}, p={p:.4f}, Cohen's d={effect_size:.3f} ({effect_interpretation})"

        return full_text if markdown else full_text.replace("\n", " ")

    explanation = make_detailed_explanation(interpret_style)

    print(explanation)
