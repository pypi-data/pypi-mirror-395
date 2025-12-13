//! built-in atproto lexicons for resolving external refs

use atrium_lex::LexiconDoc;
use std::sync::LazyLock;

/// all bundled com.atproto.* lexicons
static LEXICONS: LazyLock<Vec<LexiconDoc>> = LazyLock::new(|| {
    let mut docs = Vec::new();

    for json in LEXICON_JSON {
        if let Ok(doc) = serde_json::from_str::<LexiconDoc>(json) {
            docs.push(doc);
        }
    }

    docs.sort_by(|a, b| a.id.cmp(&b.id));
    docs
});

/// get all built-in lexicon documents
pub fn builtin_lexicons() -> &'static [LexiconDoc] {
    &LEXICONS
}

const LEXICON_JSON: &[&str] = &[
    include_str!("../lexicons/com/atproto/admin/defs.json"),
    include_str!("../lexicons/com/atproto/admin/deleteAccount.json"),
    include_str!("../lexicons/com/atproto/admin/disableAccountInvites.json"),
    include_str!("../lexicons/com/atproto/admin/disableInviteCodes.json"),
    include_str!("../lexicons/com/atproto/admin/enableAccountInvites.json"),
    include_str!("../lexicons/com/atproto/admin/getAccountInfo.json"),
    include_str!("../lexicons/com/atproto/admin/getAccountInfos.json"),
    include_str!("../lexicons/com/atproto/admin/getInviteCodes.json"),
    include_str!("../lexicons/com/atproto/admin/getSubjectStatus.json"),
    include_str!("../lexicons/com/atproto/admin/searchAccounts.json"),
    include_str!("../lexicons/com/atproto/admin/sendEmail.json"),
    include_str!("../lexicons/com/atproto/admin/updateAccountEmail.json"),
    include_str!("../lexicons/com/atproto/admin/updateAccountHandle.json"),
    include_str!("../lexicons/com/atproto/admin/updateAccountPassword.json"),
    include_str!("../lexicons/com/atproto/admin/updateSubjectStatus.json"),
    include_str!("../lexicons/com/atproto/identity/getRecommendedDidCredentials.json"),
    include_str!("../lexicons/com/atproto/identity/requestPlcOperationSignature.json"),
    include_str!("../lexicons/com/atproto/identity/resolveHandle.json"),
    include_str!("../lexicons/com/atproto/identity/signPlcOperation.json"),
    include_str!("../lexicons/com/atproto/identity/submitPlcOperation.json"),
    include_str!("../lexicons/com/atproto/identity/updateHandle.json"),
    include_str!("../lexicons/com/atproto/label/defs.json"),
    include_str!("../lexicons/com/atproto/label/queryLabels.json"),
    include_str!("../lexicons/com/atproto/label/subscribeLabels.json"),
    include_str!("../lexicons/com/atproto/moderation/createReport.json"),
    include_str!("../lexicons/com/atproto/moderation/defs.json"),
    include_str!("../lexicons/com/atproto/repo/applyWrites.json"),
    include_str!("../lexicons/com/atproto/repo/createRecord.json"),
    include_str!("../lexicons/com/atproto/repo/defs.json"),
    include_str!("../lexicons/com/atproto/repo/deleteRecord.json"),
    include_str!("../lexicons/com/atproto/repo/describeRepo.json"),
    include_str!("../lexicons/com/atproto/repo/getRecord.json"),
    include_str!("../lexicons/com/atproto/repo/importRepo.json"),
    include_str!("../lexicons/com/atproto/repo/listMissingBlobs.json"),
    include_str!("../lexicons/com/atproto/repo/listRecords.json"),
    include_str!("../lexicons/com/atproto/repo/putRecord.json"),
    include_str!("../lexicons/com/atproto/repo/strongRef.json"),
    include_str!("../lexicons/com/atproto/repo/uploadBlob.json"),
    include_str!("../lexicons/com/atproto/server/activateAccount.json"),
    include_str!("../lexicons/com/atproto/server/checkAccountStatus.json"),
    include_str!("../lexicons/com/atproto/server/confirmEmail.json"),
    include_str!("../lexicons/com/atproto/server/createAccount.json"),
    include_str!("../lexicons/com/atproto/server/createAppPassword.json"),
    include_str!("../lexicons/com/atproto/server/createInviteCode.json"),
    include_str!("../lexicons/com/atproto/server/createInviteCodes.json"),
    include_str!("../lexicons/com/atproto/server/createSession.json"),
    include_str!("../lexicons/com/atproto/server/deactivateAccount.json"),
    include_str!("../lexicons/com/atproto/server/defs.json"),
    include_str!("../lexicons/com/atproto/server/deleteAccount.json"),
    include_str!("../lexicons/com/atproto/server/deleteSession.json"),
    include_str!("../lexicons/com/atproto/server/describeServer.json"),
    include_str!("../lexicons/com/atproto/server/getAccountInviteCodes.json"),
    include_str!("../lexicons/com/atproto/server/getServiceAuth.json"),
    include_str!("../lexicons/com/atproto/server/getSession.json"),
    include_str!("../lexicons/com/atproto/server/listAppPasswords.json"),
    include_str!("../lexicons/com/atproto/server/refreshSession.json"),
    include_str!("../lexicons/com/atproto/server/requestAccountDelete.json"),
    include_str!("../lexicons/com/atproto/server/requestEmailConfirmation.json"),
    include_str!("../lexicons/com/atproto/server/requestEmailUpdate.json"),
    include_str!("../lexicons/com/atproto/server/requestPasswordReset.json"),
    include_str!("../lexicons/com/atproto/server/reserveSigningKey.json"),
    include_str!("../lexicons/com/atproto/server/resetPassword.json"),
    include_str!("../lexicons/com/atproto/server/revokeAppPassword.json"),
    include_str!("../lexicons/com/atproto/server/updateEmail.json"),
    include_str!("../lexicons/com/atproto/sync/getBlob.json"),
    include_str!("../lexicons/com/atproto/sync/getBlocks.json"),
    include_str!("../lexicons/com/atproto/sync/getCheckout.json"),
    include_str!("../lexicons/com/atproto/sync/getHead.json"),
    include_str!("../lexicons/com/atproto/sync/getLatestCommit.json"),
    include_str!("../lexicons/com/atproto/sync/getRecord.json"),
    include_str!("../lexicons/com/atproto/sync/getRepo.json"),
    include_str!("../lexicons/com/atproto/sync/getRepoStatus.json"),
    include_str!("../lexicons/com/atproto/sync/listBlobs.json"),
    include_str!("../lexicons/com/atproto/sync/listRepos.json"),
    include_str!("../lexicons/com/atproto/sync/notifyOfUpdate.json"),
    include_str!("../lexicons/com/atproto/sync/requestCrawl.json"),
    include_str!("../lexicons/com/atproto/sync/subscribeRepos.json"),
    include_str!("../lexicons/com/atproto/temp/addReservedHandle.json"),
    include_str!("../lexicons/com/atproto/temp/checkSignupQueue.json"),
    include_str!("../lexicons/com/atproto/temp/fetchLabels.json"),
    include_str!("../lexicons/com/atproto/temp/requestPhoneVerification.json"),
];
