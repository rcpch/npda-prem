def _get_saved_answer(submission, question_id):
    """Return the saved scalar answer for routing purposes, or None."""
    if submission is None:
        return None
    val = getattr(submission, question_id, None)
    # Multi-select JSONFields return lists; they are never routing answers.
    if isinstance(val, list):
        return None
    return val if val else None


def _next_step(sections, role, section_slug, question_id, submission=None):
    """
    Determine the next (section_slug, question_id) from the current position,
    using the submission's saved answer to resolve any routing.
    Returns (None, None) if the current question is the last in the survey.
    """
    current_section = next((s for s in sections if s["slug"] == section_slug), None)
    if current_section is None:
        return None, None

    role_qs = [q for q in current_section["questions"] if role in q.get("roles", [])]
    ix = next((i for i, q in enumerate(role_qs) if q["id"] == question_id), None)
    if ix is None:
        return None, None

    current_q = role_qs[ix]
    next_q_id = None
    next_s_slug = section_slug

    # 1. Routing via next_question map (uses saved answer if available)
    if "next_question" in current_q:
        opts = current_q["next_question"]
        answer = _get_saved_answer(submission, question_id)
        next_q_id = opts.get(answer) if (answer is not None and answer in opts) else opts.get("_")

    # 2. Sequential: next question in the same section
    if not next_q_id and ix + 1 < len(role_qs):
        next_q_id = role_qs[ix + 1]["id"]

    # 3. First question of the next section
    if not next_q_id:
        s_ix = next((i for i, s in enumerate(sections) if s["slug"] == section_slug), None)
        if s_ix is not None:
            for s in sections[s_ix + 1:]:
                rqs = [q for q in s["questions"] if role in q.get("roles", [])]
                if rqs:
                    next_s_slug = s["slug"]
                    next_q_id = rqs[0]["id"]
                    break

    if not next_q_id:
        return None, None  # end of survey

    # If routing jumped to a question outside the current section, find its section.
    if next_q_id not in {q["id"] for q in role_qs}:
        for s in sections:
            if any(q["id"] == next_q_id for q in s["questions"] if role in q.get("roles", [])):
                next_s_slug = s["slug"]
                break

    return next_s_slug, next_q_id


def traverse_survey(sections, role, target_section_slug, target_question_id, submission=None):
    """
    Walk from the first question using saved answers to follow routing decisions.
    Returns (position, prev_section_slug, prev_question_id), position is 1-based.
    Returns None if the target question is unreachable from the start.
    """
    current_s_slug = None
    current_q_id = None
    for s in sections:
        rqs = [q for q in s["questions"] if role in q.get("roles", [])]
        if rqs:
            current_s_slug = s["slug"]
            current_q_id = rqs[0]["id"]
            break

    if current_q_id is None:
        return None

    position = 0
    prev_s_slug = None
    prev_q_id = None
    visited = set()

    while current_q_id is not None:
        key = (current_s_slug, current_q_id)
        if key in visited:
            return None  # cycle guard
        visited.add(key)
        position += 1

        if current_s_slug == target_section_slug and current_q_id == target_question_id:
            return (position, prev_s_slug, prev_q_id)

        prev_s_slug = current_s_slug
        prev_q_id = current_q_id
        current_s_slug, current_q_id = _next_step(
            sections, role, current_s_slug, current_q_id, submission
        )

    return None  # target not found


def find_resume_question(sections, role, submission):
    """
    Walk from the first question using saved answers to follow routing, and
    return (section_slug, question_id) of the first question that has no saved
    answer — i.e. where the user should resume.
    Returns None if all reachable questions are already answered.
    """
    s_slug = None
    q_id = None
    for s in sections:
        rqs = [q for q in s["questions"] if role in q.get("roles", [])]
        if rqs:
            s_slug = s["slug"]
            q_id = rqs[0]["id"]
            break

    visited = set()
    while q_id is not None:
        key = (s_slug, q_id)
        if key in visited:
            return None
        visited.add(key)

        val = getattr(submission, q_id, None)
        is_answered = (len(val) > 0) if isinstance(val, list) else bool(val)
        if not is_answered:
            return s_slug, q_id

        s_slug, q_id = _next_step(sections, role, s_slug, q_id, submission)

    return None


def count_remaining_questions(sections, role, current_section_slug, current_question_id):
    """
    Count questions from the current (inclusive) to the end, following default
    routing (no saved answers — uses sequential or '_' fallbacks only).
    """
    count = 0
    s_slug = current_section_slug
    q_id = current_question_id
    visited = set()

    while q_id is not None:
        key = (s_slug, q_id)
        if key in visited:
            break
        visited.add(key)
        count += 1
        s_slug, q_id = _next_step(sections, role, s_slug, q_id, submission=None)

    return count
