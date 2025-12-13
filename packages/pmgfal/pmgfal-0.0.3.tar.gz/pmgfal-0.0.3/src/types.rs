//! type conversion from lexicon types to python type annotations

use std::collections::HashSet;

use atrium_lex::lexicon::{
    LexArrayItem, LexObject, LexObjectProperty, LexRecord, LexRef, LexRefUnion, LexUserType,
};
use atrium_lex::LexiconDoc;
use heck::ToPascalCase;

/// context for resolving refs within a document
pub struct RefContext<'a> {
    /// nsid of the current document (e.g., "fm.plyr.track")
    pub nsid: &'a str,
}

impl<'a> RefContext<'a> {
    pub fn new(nsid: &'a str) -> Self {
        Self { nsid }
    }

    /// resolve a ref string to a python class name
    ///
    /// - `#localDef` -> class in same document
    /// - `com.example.foo` -> external nsid main def
    /// - `com.example.foo#bar` -> external nsid specific def
    pub fn resolve_ref(&self, ref_str: &str) -> String {
        if let Some(local_name) = ref_str.strip_prefix('#') {
            // local ref within same document
            to_class_name(self.nsid, local_name)
        } else if let Some((nsid, def_name)) = ref_str.split_once('#') {
            // external ref with specific def
            to_class_name(nsid, def_name)
        } else {
            // external ref to main def
            to_class_name(ref_str, "main")
        }
    }
}

/// convert lexicon property to python type annotation
pub fn property_to_python(prop: &LexObjectProperty, ctx: &RefContext) -> String {
    match prop {
        LexObjectProperty::Boolean(_) => "bool".into(),
        LexObjectProperty::Integer(_) => "int".into(),
        LexObjectProperty::String(_) => "str".into(),
        LexObjectProperty::Bytes(_) => "bytes".into(),
        LexObjectProperty::CidLink(_) => "str".into(),
        LexObjectProperty::Blob(_) => "dict[str, Any]".into(),
        LexObjectProperty::Unknown(_) => "Any".into(),
        LexObjectProperty::Ref(r) => ref_to_python(r, ctx),
        LexObjectProperty::Union(u) => union_to_python(u, ctx),
        LexObjectProperty::Array(arr) => {
            let item_type = array_item_to_python(&arr.items, ctx);
            format!("list[{item_type}]")
        }
    }
}

/// convert a ref to python type
fn ref_to_python(r: &LexRef, ctx: &RefContext) -> String {
    ctx.resolve_ref(&r.r#ref)
}

/// convert a union to python type
fn union_to_python(u: &LexRefUnion, ctx: &RefContext) -> String {
    if u.refs.is_empty() {
        return "Any".into();
    }

    let types: Vec<String> = u.refs.iter().map(|r| ctx.resolve_ref(r)).collect();

    if types.len() == 1 {
        types.into_iter().next().unwrap()
    } else {
        types.join(" | ")
    }
}

/// convert array item type to python
fn array_item_to_python(item: &LexArrayItem, ctx: &RefContext) -> String {
    match item {
        LexArrayItem::Boolean(_) => "bool".into(),
        LexArrayItem::Integer(_) => "int".into(),
        LexArrayItem::String(_) => "str".into(),
        LexArrayItem::Bytes(_) => "bytes".into(),
        LexArrayItem::CidLink(_) => "str".into(),
        LexArrayItem::Blob(_) => "dict[str, Any]".into(),
        LexArrayItem::Unknown(_) => "Any".into(),
        LexArrayItem::Ref(r) => ref_to_python(r, ctx),
        LexArrayItem::Union(u) => union_to_python(u, ctx),
    }
}

/// generate python class name from nsid and def name
pub fn to_class_name(nsid: &str, def_name: &str) -> String {
    let mut parts: Vec<&str> = nsid.split('.').collect();
    if def_name != "main" {
        parts.push(def_name);
    }
    parts.iter().map(|p| p.to_pascal_case()).collect()
}

/// collect all external ref nsids from a document
pub fn collect_external_refs(doc: &LexiconDoc) -> HashSet<String> {
    let mut refs = HashSet::new();

    for def in doc.defs.values() {
        match def {
            LexUserType::Record(LexRecord { record, .. }) => {
                let atrium_lex::lexicon::LexRecordRecord::Object(obj) = record;
                collect_refs_from_object(obj, &mut refs);
            }
            LexUserType::Object(obj) => {
                collect_refs_from_object(obj, &mut refs);
            }
            _ => {}
        }
    }

    // filter to only external refs (not starting with #)
    refs.into_iter()
        .filter(|r| !r.starts_with('#'))
        .map(|r| {
            // extract nsid from ref (strip #defName if present)
            r.split_once('#').map(|(nsid, _)| nsid.to_string()).unwrap_or(r)
        })
        .collect()
}

fn collect_refs_from_object(obj: &LexObject, refs: &mut HashSet<String>) {
    for prop in obj.properties.values() {
        collect_refs_from_property(prop, refs);
    }
}

fn collect_refs_from_property(prop: &LexObjectProperty, refs: &mut HashSet<String>) {
    match prop {
        LexObjectProperty::Ref(r) => {
            refs.insert(r.r#ref.clone());
        }
        LexObjectProperty::Union(u) => {
            for r in &u.refs {
                refs.insert(r.clone());
            }
        }
        LexObjectProperty::Array(arr) => {
            collect_refs_from_array_item(&arr.items, refs);
        }
        _ => {}
    }
}

fn collect_refs_from_array_item(item: &LexArrayItem, refs: &mut HashSet<String>) {
    match item {
        LexArrayItem::Ref(r) => {
            refs.insert(r.r#ref.clone());
        }
        LexArrayItem::Union(u) => {
            for r in &u.refs {
                refs.insert(r.clone());
            }
        }
        _ => {}
    }
}
